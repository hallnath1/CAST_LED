# CASTLEGUARD

[![Build Status](https://travis-ci.com/hallnath1/CASTLEGUARD.svg?token=CbJDgsGLo7GCV1xLzUAy&branch=master)](https://travis-ci.com/hallnath1/CASTLEGUARD)

CASTLEGUARD (Continuously Anonymizing STreaming data via adaptive cLustEring
with GUARanteed Differential privacy) is an extension to the CASTLE data stream
anonymisation algorithm.

> Data streams are a common tool used by data controllers to outsource data
> processing of time series data to external data processors.  Data protection
> legislation now enforces that data controllers are responsible for providing
> a guarantee of privacy for user data contained within published data streams.
> CASTLE (Cao et al.) is a well-known method of anonymising data streams with a
> guarantee of k-anonymity, however, k-anonymity has been shown to be a weak
> privacy guarantee with numerous vulnerabilities in practice. As such, users
> may desire a stronger privacy guarantee. We propose Continuously Anonymising
> STreaming data via adaptive cLustEring with GUARanteed Differential privacy
> (CASTLEGUARD), a data stream anonymisation algorithm which provides a
> reliable guarantee of l-diversity and differential privacy based on
> additional parameters l, β and Φ. We achieve differential privacy for data
> streams by sampling entries from an input data stream S with probability β
> and by performing "safe" k-anonymisation, meaning that no true
> quasi-identifiable attribute value can be inferred from the extreme values of
> a generalisation, using additive noise taken from a Laplace distribution with
> μ = 0, b = (R/Φ) where R is the range of an attribute. We show that, with
> "safe" k-anonymisation and β-sampling, CASTLEGUARD satisfies differentially
> private k-anonymity. Our experimental analysis of CASTLEGUARD demonstrates
> that it effectively protects the individual privacy of users whilst still
> providing effective utility to data processors in the context of machine
> learning.

## Usage

### Command Line Simulations

The easiest way to play around with `CASTLEGUARD` is by running `src/main.py`.
This will process a stream of data from a file and display the output tuples.
Input filenames, sample sizes, random seeds and hyper-parameters can all be
configured on the command line.

For example:

```bash
python3 src/main.py --filename example.csv --sample-size 500 --k 25
```

will use `example.csv` as the input stream, pick a random sample of
`500` elements from the dataset and use a `k` value of `25`. All the options
for the interface can be seen using `python3 src/main.py -h`.

The file `example.csv` can be found in the root directory of the
project.

### Makefile Examples

A `Makefile` is also provided to give some simple examples of `CASTLEGUARD`,
along with a visualisation of the outputs. For each command, the simulation
will display the tuples and clusters still within `CASTLEGUARD`, along with the
tuples that have been output and the empty clusters.

### Advanced Examples

`CASTLEGUARD` is designed to be easy to use. It requires inputs in the form of
`pandas.Series` objects, which can be obtained by iterating through a
`pandas.DataFrame` object.

Simply add `from castle import CASTLE, Parameters` to a file in `src/`, define
the headers to use for `k-anonymity`, the header to use for `l-diversity`,
create a `Parameters` object and a callback function that takes a
`pandas.Series` object and construct your `CASTLE` object. From here, you can
simply call `CASTLE.insert(element)` to insert data. `CASTLE` will
automatically call your callback function with any generalised tuples it
produces.

#### Generalisations

Generalised data will be output with different headers to the original data.
Firstly, the `pid` column will be removed, as this is what uniquely identifies
the data subject. For each column that is to be `k`-anonymised, it will be
replaced by 3 columns.

These columns will have the name of the original, but prefixed with one of
`[min, spc, max]`. The `min` and `max` columns are the ranges of the cluster
being output, and the `spc` column is a sample value from the cluster, chosen
randomly.

The column chosen for `l`-diversity will be output as normal.

For example, the following schema with `headers = ["TripDistance"]`,
`sensitive_attribute = "FareAmount"`:

| pid | TripDistance | FareAmount |
|-----|--------------|------------|
| ... |      ...     |     ...    |

will be output to the callback function as:

| minTripDistance | spcTripDistance | maxTripDistance | FareAmount |
|-----------------|-----------------|-----------------|------------|
|       ...       |       ...       |       ...       |     ...    |

#### Available Parameters

The available parameters are as follows:

| Parameter |                         Meaning                         | Default Value|     Valid Range    |
|:---------:|:-------------------------------------------------------:|:------------:|:------------------:|
|    `k`    |        Minimum number of IDs in an output cluster       |       5      |       `k`> 0       |
|  `delta`  |         Maximum number of tuples in CASTLEGUARD         |      10      |     `delta`> 0     |
|   `beta`  |            Maximum number of active clusters            |       5      |     `beta`> 0      |
|    `mu`   |        Number of information loss values for tau        |       5      |      `mu`> 0       |
|    `l`    | Minimum number of sensitive values in an output cluster |       1      |      `l`> 0        |
|   `phi`   |                Scale of tuple pertubation               |  100 * ln(2) |      `phi`> 0      |
| `big_beta`|           1 - probability of ignoring a tuple           |       1      | 0 <=`big_beta`<= 1 |
|    `dp`   |        Whether or not to use differential privacy       |     True     |                    |

All of these can be configured either in the `Parameters` object or on the
command line.

## Unit Tests

Unit tests can be run using the `pytest` command.

### License

Licensed under either of Apache License, Version 2.0 or MIT license at your
option.
