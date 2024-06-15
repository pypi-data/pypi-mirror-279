# -*- coding: utf-8 -*-
"""
Created on Wed Dec 23 21:30:36 2020

:copyright:
    Jared Peacock (jpeacock@usgs.gov)

:license: MIT

"""
# =============================================================================
# Imports
# =============================================================================
import numpy as np

from mt_metadata.base.helpers import write_lines
from mt_metadata.base import get_schema, Base
from mt_metadata.timeseries.standards import SCHEMA_FN_PATHS
from mt_metadata.utils.exceptions import MTSchemaError

# =============================================================================
attr_dict = get_schema("filtered", SCHEMA_FN_PATHS)
# =============================================================================
class Filtered(Base):
    """
    List of filter names booleans tracking if filter has been
        applied.   May want to dict(zip(name, applied))

    """

    __doc__ = write_lines(attr_dict)

    def __init__(self, **kwargs):
        self._name = []
        self._applied = []
        self.name = None
        self.applied = None
        self.comments = None
        super().__init__(attr_dict=attr_dict, **kwargs)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, names):
        if names is None:
            self._name = []
            return

        if isinstance(names, str):
            self._name = [ss.strip().lower() for ss in names.split(",")]
        elif isinstance(names, list):
            self._name = [ss.strip().lower() for ss in names]
        elif isinstance(names, np.ndarray):
            names = names.astype(np.unicode_)
            self._name = [ss.strip().lower() for ss in names]
        else:
            msg = "names must be a string or list of strings not {0}, type {1}"
            self.logger.error(msg.format(names, type(names)))
            raise MTSchemaError(msg.format(names, type(names)))

        check = self._check_consistency()
        if not check:
            msg = (f"Filter names and applied lists are not the same size. "
                   f"Be sure to check the inputs. "
                   f"names = {self._name}, applied = {self._applied}")
            self.logger.warning(msg)

    @property
    def applied(self):
        return self._applied

    @applied.setter
    def applied(self, applied):
        if not hasattr(applied, "__iter__"):
            if applied in [None, "none", "None", "NONE", "null"]:
                self._applied = [True]
                return
            elif applied in [0, "0"]:
                self._applied = [False]
                return

        #sets an empty list to one default value
        if isinstance(applied, list) and len(applied) == 0:
            self.applied = [True]
            return

        if isinstance(applied, str):
            if applied.find("[") >= 0:
                applied = applied.replace("[", "").replace("]", "")
            if applied.count(",") > 0:
                applied_list = [
                    ss.strip().lower() for ss in applied.split(",")
                ]
            else:
                applied_list = [ss.lower() for ss in applied.split()]
        elif isinstance(applied, list):
            applied_list = applied
            # set integer strings to integers ["0","1"]--> [0, 1]
            for i, elt in enumerate(applied_list):
                if elt in ["0", "1",]:
                    applied_list[i] = int(applied_list[i])
            # set integers to bools [0,1]--> [False, True]
            for i, elt in enumerate(applied_list):
                if elt in [0, 1,]:
                    applied_list[i] = bool(applied_list[i])
        elif isinstance(applied, bool):
            applied_list = [applied]
        # the returned type from a hdf5 dataset is a numpy array.
        elif isinstance(applied, np.ndarray):
            applied_list = list(applied)
            if applied_list == []:
                applied_list = [True]
        else:
            msg = "applied must be a string or list of strings not {0}"
            self.logger.error(msg.format(applied))
            raise MTSchemaError(msg.format(applied))

        bool_list = []
        for app_bool in applied_list:
            if app_bool is None:
                bool_list.append(True)
            elif isinstance(app_bool, str):
                if app_bool.lower() in ["false", "0"]:
                    bool_list.append(False)
                elif app_bool.lower() in ["true", "1"]:
                    bool_list.append(True)
                else:
                    msg = "Filter.applied must be [ True | False ], not {0}"
                    self.logger.error(msg.format(app_bool))
                    raise MTSchemaError(msg.format(app_bool))
            elif isinstance(app_bool, (bool, np.bool_)):
                bool_list.append(bool(app_bool))
            else:
                msg = "Filter.applied must be [True | False], not {0}"
                self.logger.error(msg.format(app_bool))
        self._applied = bool_list

        # check for consistency
        check = self._check_consistency()
        if not check:
            msg = (f"Filter names and applied lists are not the same size. "
                   f"Be sure to check the inputs. "
                   f"names = {self._name}, applied = {self._applied}")
            self.logger.warning(msg)


    def _check_consistency(self):
        # check for consistency
        if self._name != []:
            if self._applied is None:
                self.logger.warning("Need to input filter.applied")
                return False
            if len(self._name) == 1:
                if len(self._applied) == 1:
                    return True
            elif len(self._name) > 1:
                if len(self._applied) == 1:
                    self.logger.debug(
                        "Assuming all filters have been "
                        + "applied as {0}".format(self._applied[0])
                    )
                    return True
                elif len(self._applied) > 1:
                    if len(self._applied) != len(self._name):
                        self.logger.warning(
                            "Applied and filter names "
                            + "should be the same length. "
                            + "Appied={0}, names={1}".format(
                                len(self._applied), len(self._name)
                            )
                        )
                        return False
                    else:
                        return True
        elif self._name == [] and len(self._applied) > 0:
            self.logger.debug("Name probably not yet initialized -- skipping consitency check")
            return True
        else:
            return False
