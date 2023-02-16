"""
Top level module for dynaddrmgr application.

Classes:
    TemplateManager
"""
import filecmp
from os import R_OK, W_OK, access
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from jinja2 import Template

from wtforglib.commander import Commander
from wtforglib.files import verify_directory
from wtforglib.fstats import set_owner_group_perms
from wtforglib.kinds import StrAnyDict
from wtforglib.options import OptionsDict
from wtforglib.scribe import Scribe
from wtforglib.versioned import unlink_path
from wtforglib.versionfile import version_file


class TemplateWriter(Commander):  # noqa: WPS214
    """
    Template generator.

    This class is responsible for managing the templates specified
    in the configuration file.
    """

    def __init__(
        self,
        opts: Optional[OptionsDict] = None,
        scribe: Optional[Scribe] = None,
    ) -> None:
        """Constructs a new instance of TemplateWriter.

        Parameters
        ----------
        opts : Optional[OptionsDict], optional
            Options dictionary, by default None
        scribe : Optional[Scribe], optional
            Scribe for logging, by default None
        """
        super().__init__(opts)
        if scribe is not None:
            self.scribe = scribe

    def generate(
        self,
        tmpl_name: str,
        tmpl_value: StrAnyDict,
        tmpl_var: StrAnyDict,
    ) -> int:
        """Generates the template if needed.

        Parameters
        ----------
        tmpl_name : str
            Template name
        tmpl_value : StrAnyDict
            Template information
        tmpl_var : StrAnyDict
            Template variable data

        Returns
        -------
        int
            Exit code
        """
        if self._verify_config_data(tmpl_name, tmpl_value):
            return self._update_template(tmpl_value, tmpl_var)
        return 1

    def _update_template(self, tmpl_value: StrAnyDict, tmpl_var: StrAnyDict) -> int:
        """Update the template if necessary.

        Parameters
        ----------
        tmpl_value : StrAnyDict
            Data describing the target file requirements
        tmpl_var : StrAnyDict
            Variables used by the template

        Returns
        -------
        int
            exit status
        """
        dest = tmpl_value.get("dest", "")
        changed = self._render_template(
            tmpl_value.get("src", ""),
            tmpl_var,
            dest,
            tmpl_value.get("backup", 0),
        )
        if changed:
            if not self.istest():
                set_owner_group_perms(
                    dest,
                    tmpl_value.get("owner", ""),
                    tmpl_value.get("group", ""),
                    tmpl_value.get("mode", ""),
                )
                cargs = tmpl_value.get("on_changed", [])
                if cargs:
                    cmdres = self.run_command(tuple(cargs))
                    return cmdres.returncode
        return 0

    def _verify_config_data(self, tmpl_name: str, tmpl_value: StrAnyDict) -> bool:
        """Verifies the configuration.

        Parameters
        ----------
        tmpl_name : str
            Name of the template
        tmpl_value : StrAnyDict
            Template values

        Returns
        -------
        bool
            True if the configuration is valid
        """
        if self._verify_template_required_keys(tmpl_name, tmpl_value):
            if self._verify_template_source(tmpl_value.get("src", "")):
                if self._verify_target(tmpl_value.get("dest", "")):
                    return True
        return False

    def _render_template(
        self,
        source: str,
        tmpl_var: StrAnyDict,
        dest: str,
        backup: int,
    ) -> bool:
        """Render the template to the file system.

        Parameters
        ----------
        source : str
            Path to the template source file
        tmpl_var : StrAnyDict
            Varible to pass into template engine
        dest : str
            Path to the output file
        backup : int
            Max number of backups to keep (if any)

        Returns
        -------
        int
            exit_code
        """
        template = Template(self._read_template_source(source))
        tfile = NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            suffix=None,
            delete=False,
        )
        tfile.write(template.render(template_dict=tmpl_var))
        tfile.close()
        return self._write_output(Path(dest), Path(tfile.name), backup)

    def _write_output(self, dpath: Path, tpath: Path, backup: int) -> bool:
        """Write output to output file, unlink temporary file.

        Parameters
        ----------
        dpath : Path
            Path to the output file
        tpath : Path
            Path to the temporary generated template file
        backup : int
            Number of backups to keep if any

        Returns
        -------
        bool : True if target file replaced
        """
        retval = False
        if dpath.exists():
            diff = filecmp.cmp(dpath, tpath)
            exists = True
        else:
            exists = False
            diff = False
        self.debug(
            "dest: {0} exists: {1} diff: {2}".format(str(dpath), exists, diff),
        )
        if not diff:
            if not self.options.get("noop", False):
                if exists:
                    self._backup_file(str(dpath), backup)
                    tpath.replace(dpath)
                else:
                    tpath.rename(dpath)
                self.info("Updated file: {0}".format(str(dpath)))
                retval = True
        if not self.isdebug():
            unlink_path(tpath, missing_ok=True)
        return retval

    def _backup_file(self, dest: str, backup: int) -> None:
        """Backup the output before replacing.

        Parameters
        ----------
        dest : str
            Path to output file.
        backup : int
            Number of backup files to keep (if any)
        """
        if backup:
            version_file(dest, "rename", backup, debug=self.isdebug())

    def _read_template_source(self, source: str) -> str:
        """Retruns the template data from the given source.

        Parameters
        ----------
        source : str
            Path to the template source

        Returns
        -------
        str
            The template data
        """
        with open(source, "r") as jinja_file:
            return jinja_file.read()

    def _verify_template_required_keys(
        self,
        tmpl_name: str,
        tmpl_value: StrAnyDict,
    ) -> bool:
        """Verify that the template required keys exist."""
        for key in ("src", "dest"):
            kv = tmpl_value.get(key)
            if kv is None:
                self.error(
                    "Template {0} does not have a {1} key!!".format(tmpl_name, key),
                )
                return False
        return True

    def _verify_target(self, dest: str) -> bool:
        """Verifies the output file.

        Parameters
        ----------
        dest : str
            Path to the output file

        Returns
        -------
        bool
            True if target directory exists and writable and file does not exist
            True if target exists, is a file, and writable
        """
        dspec = Path(dest)
        if dspec.exists():
            if not dspec.is_file():
                self.error("Template dest '{0}' not a file!!".format(dest))
                return False
            if not access(dspec, W_OK):
                self.error("Template dest '{0}' not readable!!".format(dest))
                return False
        else:
            return self._verify_target_directory(dspec.parent)
        return True

    def _verify_target_directory(self, pspec: Path) -> bool:
        """Verifies the target directory.

        Parameters
        ----------
        pspec : Path
            Path to the target directory

        Returns
        -------
        bool
            True if exists, is directory and is writable.
        """
        retval, error_message = verify_directory(pspec)
        if not retval:
            self.error(error_message)
        return retval

    def _verify_template_source(self, source: str) -> bool:
        """Verifies the template source.

        Parameters
        ----------
        source : str
            Path to the template source

        Returns
        -------
        bool
            True if source exists, is a file, is readable
        """
        spec = Path(source)
        if not spec.exists():
            self.error("Template src '{0}' not found!!".format(source))
            return False
        if not spec.is_file():
            self.error("Template src '{0}' not a file!!".format(source))
            return False
        if not access(spec, R_OK):
            self.error("Template src '{0}' not readable!!".format(source))
            return False
        return True
