from .version import __version__
import numpy as np
import copy


class DynamicSizeRecarray:
    """
    A dynamic, appendable implementation of numpy.core.records.recarray.
    """

    def __init__(self, recarray=None, dtype=None):
        """
        Either provide an existing recarray 'recarray' or
        provide the 'dtype' to start with an empty recarray.

        Parameters
        ----------
        recarray : numpy.core.records.recarray, default=None
            The start of the dynamic recarray.
        dtype : list(tuple("key", "dtype_str")), default=None
            The dtype of the dynamic recarray.
        """
        self._size = 0
        if recarray is None and dtype == None:
            raise AttributeError("Requires either 'recarray' or 'dtype'.")
        if recarray is not None and dtype is not None:
            raise AttributeError(
                "Expected either one of 'recarray' or' dtype' to be 'None'"
            )

        if dtype:
            recarray = np.core.records.recarray(
                shape=0,
                dtype=dtype,
            )

        initial_capacity = np.max([2, len(recarray)])
        self._recarray = np.core.records.recarray(
            shape=initial_capacity,
            dtype=recarray.dtype,
        )
        self.append_recarray(recarray=recarray)

    @property
    def shape(self):
        """
        Returns the appended/set shape (in number of records) of internal
        recarray.
        This is the shape a recarray will have when calling to_recarray().

        Returns
        -------
        shape : tuple(self.__len__(), )
        """
        return (self.__len__(),)

    @property
    def dtype(self):
        return self._recarray.dtype

    def _capacity(self):
        """
        Returns the capacity (in number of records) of the allocated memeory.
        This is the length of the internal recarray.
        """
        return len(self._recarray)

    def to_recarray(self):
        """
        Exports to a numpy.core.records.recarray.
        """
        out = np.core.records.recarray(
            shape=self._size,
            dtype=self._recarray.dtype,
        )
        out = self._recarray[0 : self._size]
        return out

    def append_record(self, record):
        """
        Append one record to the dynamic racarray.
        The size of the dynamic recarray will increase by one.

        Parameters
        ----------
        record : dict
            The record to be appended must have all the keys of the dynamic
            recarray. Additional keys in the reocrd will be ignored.
        """
        self._grow_if_needed(additional_size=1)
        for key in self._recarray.dtype.names:
            self._recarray[self._size][key] = record[key]
        self._size += 1

    def append_records(self, records):
        """
        Append the records to the dynamic racarray.
        The size of the dynamic recarray will increase by len(records).

        Parameters
        ----------
        record : list of dicts
            A list of records. Every record must have the keys of the internal,
            dynamic recarray.
        """
        for record in records:
            self.append_record(record=record)

    def append_recarray(self, recarray):
        """
        Append a recarray to the dynamic racarray.
        The size of the dynamic recarray will increase by len(recarray).

        Parameters
        ----------
        recarray : numpy.core.records.recarray
            This will be appended to the internal, dynamic recarray.
        """
        self._grow_if_needed(additional_size=len(recarray))
        start = self._size
        stop = start + len(recarray)
        self._recarray[start:stop] = recarray
        self._size += len(recarray)

    def _grow_if_needed(self, additional_size):
        assert additional_size >= 0
        current_capacity = self._capacity()
        required_size = self._size + additional_size

        if required_size > current_capacity:
            swp = copy.deepcopy(self._recarray)
            next_capacity = np.max([current_capacity * 2, required_size])
            self._recarray = np.core.records.recarray(
                shape=next_capacity,
                dtype=swp.dtype,
            )
            start = 0
            stop = self._size
            self._recarray[start:stop] = swp[0 : self._size]
            del swp

    def _raise_IndexError_if_out_of_bounds(self, idx):
        if idx >= self._size:
            raise IndexError(
                "index {:d} is out of bounds for size {:d}".format(
                    idx, self._size
                )
            )

    def tobytes(self):
        return self.to_recarray().tobytes()

    def __getitem__(self, idx):
        if isinstance(idx, str):
            return self._getitem_by_column_key_str(key=idx)
        else:
            return self._getitem_by_row_idx_int(idx=idx)

    def __setitem__(self, idx, value):
        self._raise_IndexError_if_out_of_bounds(idx=idx)
        self._recarray[idx] = value

    def _getitem_by_column_key_str(self, key):
        return self._recarray[key][0 : self.__len__()]

    def _getitem_by_row_idx_int(self, idx):
        self._raise_IndexError_if_out_of_bounds(idx=idx)
        return self._recarray[idx]

    def __len__(self):
        return self._size

    def __repr__(self):
        out = "{:s}(dtype={:s})".format(
            self.__class__.__name__, str(self._recarray.dtype.descr)
        )
        return out
