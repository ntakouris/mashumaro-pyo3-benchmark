use pyo3::prelude::*;
use pyo3::types::PyBytes;

extern crate serde;
#[macro_use]
extern crate serde_derive;
use serde::{Serialize};

use serde_json;

extern crate rmp_serde as rmps;


use std::convert::{TryFrom, TryInto};

// There is no support for enums in pyo3
// plus, Currency is more like a constants container rather than enum
// (and to be honest structural pattern matching for python just arrived)
#[pyclass]
#[derive(Debug, PartialEq, Deserialize, Serialize, Clone)]
pub struct Currency {
    #[pyo3(get, set)]
    currency: String
}

#[pymethods]
impl Currency {
    #[new]
    pub fn new(currency: String) -> Self {
        Currency {
            currency
        }
    }
}

#[pyclass]
#[derive(Debug, PartialEq, Deserialize, Serialize, Clone)]
pub struct CurrencyPosition {
    #[serde(flatten)]
    #[pyo3(get, set)]
    pub currency: Currency,
    #[pyo3(get, set)]
    pub balance: f32,
}

#[pymethods]
impl CurrencyPosition {
    #[new]
    pub fn new(currency: Currency, balance: f32) -> Self {
        CurrencyPosition {
            currency,
            balance,
        }
    }
}


#[pyclass]
#[derive(Debug, PartialEq, Deserialize, Serialize, Clone)]
pub struct StockPosition {
    #[pyo3(get, set)]
    pub ticker: String,
    #[pyo3(get, set)]
    pub name: String,
    #[pyo3(get, set)]
    pub balance: i32,
}

#[pymethods]
impl StockPosition {
    #[new]
    pub fn new(ticker: String, name: String, balance: i32) -> Self {
        StockPosition {
            ticker,
            name,
            balance,
        }
    }
}

#[pyclass]
#[derive(Debug, PartialEq, Deserialize, Serialize, Clone)]
pub struct Portfolio {
    #[pyo3(get, set)]
    pub currencies: Vec<CurrencyPosition>,
    #[pyo3(get, set)]
    pub stocks:  Vec<StockPosition>,
}

#[pymethods]
impl Portfolio {
    #[new]
    pub fn new(currencies: Vec<CurrencyPosition>, stocks:  Vec<StockPosition>) -> Self {
        Portfolio {
            currencies,
            stocks,
        }
    }

    #[staticmethod]
    pub fn from_json(payload: String) -> Option<Self> {
        serde_json::from_str::<Portfolio>(&payload.as_str()).ok()
    }

    pub fn to_json(&self) -> Option<String> {
        serde_json::to_string(self).ok()
    }

    #[staticmethod]
    pub fn from_msgpack(bytes: &PyBytes) -> Option<Self> {
        let bytes_slice = bytes.as_bytes();

        Portfolio::try_from(bytes_slice.to_vec()).ok()
    }

    pub fn to_msgpack(&self, py: Python) -> Option<PyObject> {
        let buf: Result<Vec<u8>, rmps::encode::Error> = self.try_into();

        buf.to_pybytes(py)
    }
}

// msgpack
impl TryFrom<Vec<u8>> for Portfolio {
    type Error = rmps::decode::Error;

    fn try_from(bytes: Vec<u8>) -> Result<Self, Self::Error> {
        Ok(rmps::from_read_ref(bytes.as_slice())?)
    }
}

impl TryFrom<&Portfolio> for Vec<u8> {
    type Error = rmps::encode::Error;

    fn try_from(ptu_state: &Portfolio) -> Result<Self, Self::Error> {
        let mut buf = Vec::new();
        let _serialized =
            ptu_state.serialize(&mut rmps::Serializer::new(&mut buf).with_struct_map())?;

        Ok(buf)
    }
}

pub trait ToPyBytesOption {
    fn to_pybytes(&self, py: Python) -> Option<PyObject>;
}

impl ToPyBytesOption for Result<Vec<u8>, rmps::encode::Error> {
    fn to_pybytes(&self, py: Python) -> Option<PyObject> {
        match self {
            Ok(buf) => Some(PyBytes::new(py, &buf.as_slice()).into()),
            Err(_) => None,
        }
    }
}

#[pymodule]
fn schema_rs(_py: Python, module: &PyModule) -> PyResult<()> {
    module.add_class::<Currency>()?;
    module.add_class::<CurrencyPosition>()?;
    module.add_class::<StockPosition>()?;
    module.add_class::<Portfolio>()?;

    Ok(())
}
