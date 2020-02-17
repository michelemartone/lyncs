
from .tunable import Tunable

class Field(Tunable):
    _field_types = {
        "scalar": ["dims"],
        "vector": ["dims", "dofs"],
        "propagator": ["vector", "dofs"],
        "gauge": ["dims", "gauge_dofs", "gauge_dofs"],
        "gauge_links": ["gauge", "n_dims"],
        }
    
    
    def __init__(
            self,
            array = None,
            lattice = None,
            field_type = None,
            tunable_options = {},
            tuned_options = {},
    ):
        """
        A field defined on the lattice.
        
        Parameters
        ----------
        array : array_like
            Values for this field. Must be an ``numpy.ndarray``, ndarray like,
            or castable to an ``ndarray``. A view of the array's data is used
            instead of a copy if possible. If instead it is alreadt a field 
            object, then a copy of the field is made.
        lattice: Lattice object.
            The lattice on which the field is defined.
        field_type: str or list(str).
          --> If str, then must be one of the labeled field types. See Field._field_types
          --> If list, then a list of variables of lattice.
        tunable_options: dict
           List of tunable parameters with default values.
           Tunable options are attributes of the field and can be used to condition the computation. 
        tuned_options: dict
           Same as tunable options but with a fixed value.
        """
        self.lattice = lattice or array.lattice
        self.field_type = field_type or array.field_type
        self.array = array
        
        from .tunable import Permutation
        
        Tunable.__init__(self,
                         shape_order = Permutation([v[0] for v in self.shape]),
                         **tunable_options,
                         **tuned_options)
        for key,val in tuned_options.items(): setattr(self,key,val)


    @property
    def lattice(self):
        try:
            return self._lattice
        except:
            return None
        
    @lattice.setter
    def	lattice(self, value):
        assert self.lattice is None, "Not allowed to change lattice, if needed ask to implement it"
        from .lattice import Lattice
        assert isinstance(value, Lattice)
        
        self._lattice = value

        
    @property
    def dtype(self):
        return self.lattice.dtype


    @property
    def dims(self):
        return [key for key,size in self.shape if key in self.lattice.dims]

    
    @property
    def dofs(self):
        return [key for key,size in self.shape if key in self.lattice.dofs]
    
    
    @property
    def field_type(self):
        try:
            return self._field_type
        except:
            return None

    @field_type.setter
    def	field_type(self, value):
        assert self.field_type is None, "Not allowed to change field_type, if needed ask to implement it"
        def is_known(self, key):
            if isinstance(key, (list, tuple)):
                return all(is_known(self,k) for k in key)
            elif isinstance(key, str):
                return key in self.lattice.__dir__() or key in self._field_types
            else:
                assert False, "Got key that is neither list or str, %s" % key
                
        assert is_known(self, value), "Got unknown field type"
        self._field_type = value


    @property
    def array(self):
        try:
            return self._array
        except:
            return None

    @array.setter
    def array(self, value):
        if value is None:
            self.zeros()
        else:
            self._array = value


    @property
    def shape(self):
        """
        Returns the list of dimensions with size. The order is not significant.
        """
        def get_shape(self, key):
            if isinstance(key, (list, tuple)):
                ret = []
                for k in key:
                    ret += get_shape(self,k)
                return ret
            elif isinstance(key, dict):
                assert all(isinstance(value, int) for value in key.values())
                return list(key.items())
            elif isinstance(key, str):
                if key in self.lattice.__dir__():
                    value = getattr(self.lattice, key)
                elif key in self._field_types:
                    value = self._field_types[key]
                else:
                    assert False, "Unknown attribute %s"%key
                if isinstance(value, int):
                    return [(key, value)]
                else:
                    return get_shape(self,value)
            else:
                assert False, "Got key that is neither list or str, %s" % key
                
        return get_shape(self, self.field_type)


    @property
    def size(self):
        """
        Returns the number of elements in the field.
        """
        prod = 1
        for t in self.shape: prod*=t[1]
        return prod


    @property
    def byte_size(self):
        """
        Returns the size of the field in bytes
        """
        return self.size*self.dtype.itemsize
    
        
    def load(
            self,
            filename,
            format = None,
            **info,
    ):
        """
        Loads data from file.
        
        Parameters
        ----------
        filename: (str) path and filename of the data file to read.
        format: (str) format of the file to read (see load for help).
        info: information needed to perform the reading.
        """
        from .io import get_reading_info, read_data
        from dask import delayed
        info = get_reading_info(filename, format=format, field=self, **info)
        self.array = delayed(read_data)(info)
        

    def save(
            filename,
            format = None,
            **info,
    ):
        """
        Saves data into file.
        
        Parameters
        ----------
        filename: (str) path and filename of the data file to save.
        format: (str) format of the file to save (see load for help).
        info: information needed to perform the writing.
        """
        from .io import save_field
        save(self, fielname, format=format, field=overwrite)


    def zeros(self):
        """
        Initialize the field with zeros.
        """
        from .tunable import delayed
        from dask.array import zeros
        tuned = delayed(self)
        self.array = delayed(zeros)(
            shape = tuned.array_shape,
            chuncks = tuned.chuncks,
            dtype = tuned.dtype,
        )


    def __repr__(self):
        from .utils import default_repr
        return default_repr(self)
    
