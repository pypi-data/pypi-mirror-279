# Changelog

## [Unreleased]

## [2.4.1]

- Bugfix for typo in CompatibilityGraph.exchangeEdges

## [2.4.0]

- Add PICEF model

## [2.3.1]

- Add ability to output CompatibilityGraph in DOT graph format
- Add an option `build_alt_embed` to models that can be set to 0 (for no
    alternate or embedded cycles), 1 (for all alternate and embedded cycles) and
    2 and 3 (two ways of restricting alternate and embedded cycles to those
    expected by NHSBT).
    For more precise details on what this means, see the documentation for
    `build_alternates_and_embeds` in `kep_solver/graph.py`.
- Add UKXML output format
- Allow for floating-point inaccuracies when checking validity of distributions
    for dataset generators.

## [2.3.0]

- API changes to models - maxCycleLength and maxChainLength must now be
    specified as keyword arguments.
- Add status field for donors and recipients. Only donors and recipients who are
    "InPool" can be in a matching run. Note that if a donor is "InPool" but
    their paired recipient is not, then the donor still won't be in the matching
    run (and vice-versa if all of a recipient's donors are not "InPool")
- Add a new YAML format. In particular, this format allows recipient identifiers
    to be arbitrary strings, instead of just integers.

## [2.2.0]

- Add ability to count number of solutions at each objective step
- Calculate time taken to solve each individual objective
- Move to pyproject.toml completely for builds, and using the build package to
	actually build. This is required as setuptools is being deprecated.
- Allow a user to specify how ID strings for Donors and Recipients should be
	generated when generating random instances.
- Add Instance.writeFileXml() to write to XML.

## [2.1.3]

- Add Instance.writeFile() and Instance.writeFileJson() methods for writing
	instances to files. So far only the NHSBT JSON format is supported.
- Fix DonorCountGenerator to not expect integers as keys in JSON. JSON doesn't
	allow integers as keys, so expect the keys to be string representations of
	integers instead.
- Fix reading of FloatGenerator from JSON when a single floating point number
	has a chance of occuring.

## [2.1.2]

- RecipientGenerator now links a donor to their recipient correctly
- CompatibilityGraph.findCycles() speed-ups
- CompatibilityGraph.findChains() speed-ups
- Cache Vertex.adjacent() list and hash(Exchange)
- Update python version for notebooks
- Added prototype functions to Model superclass for getting cycles, chains,
	exchanges, and getting exchange values. These obviously might not be easily
	implementable by all models, and may be left unimplemented.

## [2.1.1]

- Documentation updates

## [2.1.0]

- Create random entity generators. Each of these can generate random instances
	according to some given configuration. The configuration of each can be read
	from a JSON object, and also be written to a JSON object (with the exception
	of CompatibilityChanceGenerator when a function is used to define the
	distribution to use). These items can also nested (e.g., the
	RecipientGenerator includes a DonorGenerator object) and will automatically
	export the configurations of nested generators. The complete list of
	generators added is:
	* BloodGroupGenerator
	* DonorGenerator
	* DonorCountGenerator
	* FloatGenerator (can be used for cPRA or compatibility chance)
	* cPRAGenerator
	* CompatibilityChanceGenerator
	* RecipientGenerator
	* InstanceGenerator
- Create InstanceSet entity. This stores a set of Instance objects, and can
	also calculate the compatibility chance for recipients. There are also
	helpful functions to output all donor or recipient information into a Pandas
	dataframe for statistical analysis.
- Instance: Add ability to add pre-constructed recipients
- Add underscores to string representations to separate object type and ID
- Add CompatibilityChance to Recipient class. This represents the chance that
	this Recipient will be compatible with a Donor, assuming that the two are
	ABO compatible.
- Move BloodGroup functions into the class

## [2.0.12]

- Fixed bug with single altruistic donors (i.e. chains containing just an
	altruistic donor) counting as containing an effective two-way exchange.

## [2.0.11]

- Add documentation of output format

## [2.0.10]

- Bug fixes for the JSON output.

## [2.0.9]

- Add support for JSON output (in UK style). This involved some refactoring, as
	this output needs to know the model used to solve an instance.
- Add tests for JSON output
- pool.Pool objects now must have a string description
- pool.Pool exposes maxCycleLength and maxChainLength as properties
- pool.solve\_single() now returns a Solution and the Model used to find it
- model.UK\_age\_score(): Move the UK age scoring into its own function
- Hide pulp warnings on overwriting objectives

## [2.0.8]

- More fixes for backarcs. Make sure that a backarc exchange only has two
	vertices in it, otherwise we might accidentally catch a long chain in the
	reverse direction.
- EffectiveTwoWay: Chains should be counted.

## [2.0.7]

- The CycleAndChainModel needs all cycles and exchanges to have unique IDs, so
	force this.
- Accidentally missed version 2.0.6

## [2.0.5]

- Another backarc calculation fix. Each arc should have at most one "backarc"
	exchange, even if there are multiple other exchanges that could match the
	correct recipients (due to some of said recipients having multiple donors).

## [2.0.4]

- Equality comparisons of exchanges only considers exchange IDs now
- Fix backarc calculation. Backarcs can use different donors, but must have the
	right recipients

## [2.0.3]

- Fix error with Pulp and empty objectives

## [2.0.2]

- Rework UK backarcs. To match existing code, these are implemented in a
	specific manner.
- Alternate and embedded exchanges for cycles must be cycles, and alternate and
	embedded exchanges for chains must be chains that use the same non-directed
	donor
- Add __repr__ to Donor

## [2.0.0]

- New class for Exchange objects
- Add build\_alternates\_and\_embeds() function to find alternate and embedded
	cycles
- Update documentation to add example of CompatibiltyGraph usage
- Moved to [Black](https://black.readthedocs.io/en/stable/) for formatting

## [1.0.4]

- Use setuptools\_scm for versioning

## [1.0.3]

- Fix continuous deployment

## [1.0.2]

- Fix documentation

## [1.0.1]

- Add ability to read blood groups of donors and recipients
- Add Recipient.pairedWith(Donor) function
- Add custom exceptions for data IO
- Allow variations of bloodgroup/bloodtype in input
- Allow variations of cPRA/PRA/cpra in input
- Add functions for blood group compatibility checks to Donor and Recipient

## [1.0.0]

First release
