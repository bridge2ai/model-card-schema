-- # Class: Version Description: Version information for a model
--     * Slot: id
--     * Slot: name Description: Version identifier (e.g., '1.0.0', 'v2', 'beta')
--     * Slot: date Description: Release date of this version
--     * Slot: diff Description: Changes from the previous version
-- # Class: License Description: License information (use SPDX identifier OR custom text, not both)
--     * Slot: id
--     * Slot: identifier Description: SPDX license identifier (e.g., 'Apache-2.0', 'MIT', 'CC-BY-4.0')
--     * Slot: custom_text Description: Custom license text (use when SPDX identifier is not applicable)
-- # Class: owner Description: Model owner or maintainer information
--     * Slot: id
--     * Slot: name Description: Name of the owner (individual or organization)
--     * Slot: contact Description: Contact information (email, website, etc.)
-- # Class: Reference Description: Reference to related resources
--     * Slot: id
--     * Slot: reference Description: URL or citation string for related resource
-- # Class: Citation Description: Citation information for the model
--     * Slot: id
--     * Slot: style Description: Citation format style
--     * Slot: citation Description: Formatted citation text
-- # Class: ModelDetails Description: Comprehensive metadata about the model
--     * Slot: id
--     * Slot: name Description: Model name or identifier
--     * Slot: overview Description: High-level description of what the model does
--     * Slot: documentation Description: Detailed documentation and usage guide
--     * Slot: path Description: Storage location or path to model artifacts
--     * Slot: version_id Description: Version information
-- # Class: SensitiveData Description: Information about sensitive data in a dataset
--     * Slot: id
-- # Class: GraphicsCollection Description: Collection of graphics and visualizations
--     * Slot: id
--     * Slot: description Description: Description of this graphics collection
-- # Class: graphic Description: A single graphic or visualization
--     * Slot: id
--     * Slot: name Description: Name or title of the graphic
--     * Slot: image Description: Base64-encoded PNG image
-- # Class: dataSet Description: Information about a dataset used for training or evaluation
--     * Slot: id
--     * Slot: name Description: Dataset name or identifier
--     * Slot: description Description: Dataset overview and characteristics
--     * Slot: link Description: URL to the dataset
--     * Slot: bias_input Description: Known biases present in the input data
--     * Slot: unit Description: Unit for values in this dataset
--     * Slot: sensitive_id Description: Sensitive data information
--     * Slot: graphics_id Description: Visualizations of the dataset
-- # Class: KeyVal Description: Key-value pair for format mappings
--     * Slot: id
--     * Slot: key Description: Key identifier
--     * Slot: value Description: Value associated with the key
-- # Class: ModelParameters Description: Parameters and specifications for model construction
--     * Slot: id
--     * Slot: model_architecture Description: Model architecture specification and description
--     * Slot: input_format Description: Plain text description of input format
--     * Slot: output_format Description: Plain text description of output format
-- # Class: ConfidenceInterval Description: Confidence interval for a metric value
--     * Slot: id
--     * Slot: lower_bound Description: Lower bound of the confidence interval
--     * Slot: upper_bound Description: Upper bound of the confidence interval
-- # Class: performanceMetric Description: A performance metric with optional confidence interval
--     * Slot: id
--     * Slot: type Description: Type of performance metric (e.g., 'accuracy', 'F1', 'AUC', 'precision')
--     * Slot: value Description: Metric value
--     * Slot: value_error Description: Estimated error for the metric value
--     * Slot: threshold Description: Decision threshold used when computing this metric
--     * Slot: slice Description: Data slice or subset this metric was computed on
--     * Slot: unit Description: Unit for the metric value, if applicable
--     * Slot: confidence_interval_id Description: Confidence interval for the metric
-- # Class: QuantitativeAnalysis Description: Quantitative analysis and performance evaluation of the model
--     * Slot: id
--     * Slot: graphics_id Description: Performance visualizations and plots
-- # Class: User Description: Description of an intended user type
--     * Slot: id
--     * Slot: description Description: Description of the intended user type or role
-- # Class: UseCase Description: Description of a use case or application scenario
--     * Slot: id
--     * Slot: description Description: Description of the application scenario
-- # Class: Limitation Description: A known limitation or constraint of the model
--     * Slot: id
--     * Slot: description Description: Description of the limitation or constraint
-- # Class: Tradeoff Description: A performance tradeoff consideration
--     * Slot: id
--     * Slot: description Description: Description of the performance tradeoff
-- # Class: risk Description: An ethical, environmental, or operational risk
--     * Slot: id
--     * Slot: name Description: Name or type of the risk
--     * Slot: mitigation_strategy Description: Strategy used to address or mitigate this risk
-- # Class: Considerations Description: Considerations for model usage including limitations and ethical concerns
--     * Slot: id
-- # Class: Task Description: ML task specification for benchmarking
--     * Slot: id
--     * Slot: type Description: Task type identifier (e.g., 'text-generation', 'image-classification')
--     * Slot: name Description: Human-readable task name
-- # Class: BenchmarkDataset Description: Dataset used for benchmarking
--     * Slot: id
--     * Slot: type Description: Dataset type identifier
--     * Slot: name Description: Dataset name
--     * Slot: config Description: Dataset configuration
--     * Slot: split Description: Dataset split (train, test, validation)
--     * Slot: revision Description: Dataset version or revision
--     * Slot: args Description: Additional arguments for dataset loading
-- # Class: BenchmarkMetric Description: Benchmark metric result
--     * Slot: id
--     * Slot: type Description: Metric type identifier
--     * Slot: value Description: Metric value
--     * Slot: name Description: Metric name
--     * Slot: config Description: Metric configuration
--     * Slot: args Description: Additional metric arguments
-- # Class: BenchmarkSource Description: Source of benchmark results
--     * Slot: id
--     * Slot: name Description: Source name (e.g., 'Open LLM Leaderboard', 'GLUE Benchmark')
--     * Slot: url Description: URL to the source
-- # Class: BenchmarkResult Description: Benchmark result entry with task, dataset, and metrics
--     * Slot: id
--     * Slot: task_id Description: Task that was evaluated
--     * Slot: dataset_id Description: Dataset used for evaluation
--     * Slot: source_id Description: Source of the benchmark results
-- # Class: ModelIndex Description: Papers with Code model-index structure for benchmark tracking
--     * Slot: id
--     * Slot: name Description: Model name for this benchmark entry
-- # Class: modelCard Description: Complete model card with metadata, performance, and considerations
--     * Slot: id
--     * Slot: schema_version Description: Version of the model card schema being used
--     * Slot: model_category Description: Category or parent class of the model
--     * Slot: bias_model Description: Known biases in the model itself
--     * Slot: bias_output Description: Known biases in the model's outputs
--     * Slot: framework Description: ML framework used (TensorFlow, PyTorch, JAX, Scikit-Learn, etc.)
--     * Slot: framework_version Description: Version of the ML framework
--     * Slot: library_name Description: Library name for loading the model (e.g., transformers, diffusers, timm)
--     * Slot: pipeline_tag Description: Task type for pipeline usage
--     * Slot: base_model Description: Parent model identifier (for fine-tuned or derived models)
--     * Slot: model_details_id Description: Comprehensive model metadata and details
--     * Slot: model_parameters_id Description: Model construction and architecture parameters
--     * Slot: quantitative_analysis_id Description: Quantitative analysis and performance evaluation
--     * Slot: considerations_id Description: Usage considerations, limitations, and ethical concerns
-- # Class: ModelDetails_owners
--     * Slot: ModelDetails_id Description: Autocreated FK slot
--     * Slot: owners_id Description: Model owners or maintainers
-- # Class: ModelDetails_licenses
--     * Slot: ModelDetails_id Description: Autocreated FK slot
--     * Slot: licenses_id Description: Licensing information
-- # Class: ModelDetails_references
--     * Slot: ModelDetails_id Description: Autocreated FK slot
--     * Slot: references_id Description: References to related resources
-- # Class: ModelDetails_citations
--     * Slot: ModelDetails_id Description: Autocreated FK slot
--     * Slot: citations_id Description: How to cite this model
-- # Class: SensitiveData_sensitive_data
--     * Slot: SensitiveData_id Description: Autocreated FK slot
--     * Slot: sensitive_data Description: Types of PII or sensitive information (e.g., names, addresses, medical records)
-- # Class: GraphicsCollection_collection
--     * Slot: GraphicsCollection_id Description: Autocreated FK slot
--     * Slot: collection_id Description: Graphics in this collection
-- # Class: ModelParameters_data
--     * Slot: ModelParameters_id Description: Autocreated FK slot
--     * Slot: data_id Description: Training and evaluation datasets
-- # Class: ModelParameters_input_format_map
--     * Slot: ModelParameters_id Description: Autocreated FK slot
--     * Slot: input_format_map_id Description: Structured mapping of input format fields
-- # Class: ModelParameters_output_format_map
--     * Slot: ModelParameters_id Description: Autocreated FK slot
--     * Slot: output_format_map_id Description: Structured mapping of output format fields
-- # Class: QuantitativeAnalysis_performance_metrics
--     * Slot: QuantitativeAnalysis_id Description: Autocreated FK slot
--     * Slot: performance_metrics_id Description: Performance metrics and evaluation results
-- # Class: Considerations_users
--     * Slot: Considerations_id Description: Autocreated FK slot
--     * Slot: users_id Description: Intended user types
-- # Class: Considerations_use_cases
--     * Slot: Considerations_id Description: Autocreated FK slot
--     * Slot: use_cases_id Description: Intended use cases and application scenarios
-- # Class: Considerations_limitations
--     * Slot: Considerations_id Description: Autocreated FK slot
--     * Slot: limitations_id Description: Known limitations and constraints
-- # Class: Considerations_tradeoffs
--     * Slot: Considerations_id Description: Autocreated FK slot
--     * Slot: tradeoffs_id Description: Performance tradeoffs to consider
-- # Class: Considerations_ethical_considerations
--     * Slot: Considerations_id Description: Autocreated FK slot
--     * Slot: ethical_considerations_id Description: Ethical considerations and identified risks
-- # Class: BenchmarkResult_metrics
--     * Slot: BenchmarkResult_id Description: Autocreated FK slot
--     * Slot: metrics_id Description: Metrics reported for this benchmark
-- # Class: ModelIndex_results
--     * Slot: ModelIndex_id Description: Autocreated FK slot
--     * Slot: results_id Description: Benchmark results
-- # Class: modelCard_language
--     * Slot: modelCard_id Description: Autocreated FK slot
--     * Slot: language Description: Natural language(s) processed by the model
-- # Class: modelCard_tags
--     * Slot: modelCard_id Description: Autocreated FK slot
--     * Slot: tags Description: Searchable keywords and tags for discovery
-- # Class: modelCard_datasets
--     * Slot: modelCard_id Description: Autocreated FK slot
--     * Slot: datasets Description: Training dataset identifiers or names
-- # Class: modelCard_metrics
--     * Slot: modelCard_id Description: Autocreated FK slot
--     * Slot: metrics Description: Evaluation metrics used for this model
-- # Class: modelCard_model_index
--     * Slot: modelCard_id Description: Autocreated FK slot
--     * Slot: model_index_id Description: Benchmark results following Papers with Code model-index format

CREATE TABLE "Version" (
	id INTEGER NOT NULL,
	name TEXT,
	date DATE,
	diff TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Version_id" ON "Version" (id);
CREATE TABLE "License" (
	id INTEGER NOT NULL,
	identifier TEXT,
	custom_text TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_License_id" ON "License" (id);
CREATE TABLE owner (
	id INTEGER NOT NULL,
	name TEXT,
	contact TEXT,
	PRIMARY KEY (id)
);CREATE INDEX ix_owner_id ON owner (id);
CREATE TABLE "Reference" (
	id INTEGER NOT NULL,
	reference TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Reference_id" ON "Reference" (id);
CREATE TABLE "Citation" (
	id INTEGER NOT NULL,
	style VARCHAR(7),
	citation TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Citation_id" ON "Citation" (id);
CREATE TABLE "SensitiveData" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_SensitiveData_id" ON "SensitiveData" (id);
CREATE TABLE "GraphicsCollection" (
	id INTEGER NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_GraphicsCollection_id" ON "GraphicsCollection" (id);
CREATE TABLE graphic (
	id INTEGER NOT NULL,
	name TEXT,
	image TEXT,
	PRIMARY KEY (id)
);CREATE INDEX ix_graphic_id ON graphic (id);
CREATE TABLE "KeyVal" (
	id INTEGER NOT NULL,
	"key" TEXT,
	value TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_KeyVal_id" ON "KeyVal" (id);
CREATE TABLE "ModelParameters" (
	id INTEGER NOT NULL,
	model_architecture TEXT,
	input_format TEXT,
	output_format TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_ModelParameters_id" ON "ModelParameters" (id);
CREATE TABLE "ConfidenceInterval" (
	id INTEGER NOT NULL,
	lower_bound FLOAT,
	upper_bound FLOAT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_ConfidenceInterval_id" ON "ConfidenceInterval" (id);
CREATE TABLE "User" (
	id INTEGER NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_User_id" ON "User" (id);
CREATE TABLE "UseCase" (
	id INTEGER NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_UseCase_id" ON "UseCase" (id);
CREATE TABLE "Limitation" (
	id INTEGER NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Limitation_id" ON "Limitation" (id);
CREATE TABLE "Tradeoff" (
	id INTEGER NOT NULL,
	description TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Tradeoff_id" ON "Tradeoff" (id);
CREATE TABLE risk (
	id INTEGER NOT NULL,
	name TEXT,
	mitigation_strategy TEXT,
	PRIMARY KEY (id)
);CREATE INDEX ix_risk_id ON risk (id);
CREATE TABLE "Considerations" (
	id INTEGER NOT NULL,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Considerations_id" ON "Considerations" (id);
CREATE TABLE "Task" (
	id INTEGER NOT NULL,
	type TEXT,
	name TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_Task_id" ON "Task" (id);
CREATE TABLE "BenchmarkDataset" (
	id INTEGER NOT NULL,
	type TEXT,
	name TEXT,
	config TEXT,
	split TEXT,
	revision TEXT,
	args TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_BenchmarkDataset_id" ON "BenchmarkDataset" (id);
CREATE TABLE "BenchmarkMetric" (
	id INTEGER NOT NULL,
	type TEXT,
	value FLOAT,
	name TEXT,
	config TEXT,
	args TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_BenchmarkMetric_id" ON "BenchmarkMetric" (id);
CREATE TABLE "BenchmarkSource" (
	id INTEGER NOT NULL,
	name TEXT,
	url TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_BenchmarkSource_id" ON "BenchmarkSource" (id);
CREATE TABLE "ModelIndex" (
	id INTEGER NOT NULL,
	name TEXT,
	PRIMARY KEY (id)
);CREATE INDEX "ix_ModelIndex_id" ON "ModelIndex" (id);
CREATE TABLE "ModelDetails" (
	id INTEGER NOT NULL,
	name TEXT NOT NULL,
	overview TEXT,
	documentation TEXT,
	path TEXT,
	version_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(version_id) REFERENCES "Version" (id)
);CREATE INDEX "ix_ModelDetails_id" ON "ModelDetails" (id);
CREATE TABLE "dataSet" (
	id INTEGER NOT NULL,
	name TEXT,
	description TEXT,
	link TEXT NOT NULL,
	bias_input TEXT,
	unit TEXT,
	sensitive_id INTEGER,
	graphics_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(sensitive_id) REFERENCES "SensitiveData" (id),
	FOREIGN KEY(graphics_id) REFERENCES "GraphicsCollection" (id)
);CREATE INDEX "ix_dataSet_id" ON "dataSet" (id);
CREATE TABLE "performanceMetric" (
	id INTEGER NOT NULL,
	type TEXT NOT NULL,
	value FLOAT,
	value_error FLOAT,
	threshold FLOAT,
	slice TEXT,
	unit TEXT,
	confidence_interval_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(confidence_interval_id) REFERENCES "ConfidenceInterval" (id)
);CREATE INDEX "ix_performanceMetric_id" ON "performanceMetric" (id);
CREATE TABLE "QuantitativeAnalysis" (
	id INTEGER NOT NULL,
	graphics_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(graphics_id) REFERENCES "GraphicsCollection" (id)
);CREATE INDEX "ix_QuantitativeAnalysis_id" ON "QuantitativeAnalysis" (id);
CREATE TABLE "BenchmarkResult" (
	id INTEGER NOT NULL,
	task_id INTEGER,
	dataset_id INTEGER,
	source_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(task_id) REFERENCES "Task" (id),
	FOREIGN KEY(dataset_id) REFERENCES "BenchmarkDataset" (id),
	FOREIGN KEY(source_id) REFERENCES "BenchmarkSource" (id)
);CREATE INDEX "ix_BenchmarkResult_id" ON "BenchmarkResult" (id);
CREATE TABLE "SensitiveData_sensitive_data" (
	"SensitiveData_id" INTEGER,
	sensitive_data TEXT,
	PRIMARY KEY ("SensitiveData_id", sensitive_data),
	FOREIGN KEY("SensitiveData_id") REFERENCES "SensitiveData" (id)
);CREATE INDEX "ix_SensitiveData_sensitive_data_SensitiveData_id" ON "SensitiveData_sensitive_data" ("SensitiveData_id");CREATE INDEX "ix_SensitiveData_sensitive_data_sensitive_data" ON "SensitiveData_sensitive_data" (sensitive_data);
CREATE TABLE "GraphicsCollection_collection" (
	"GraphicsCollection_id" INTEGER,
	collection_id INTEGER,
	PRIMARY KEY ("GraphicsCollection_id", collection_id),
	FOREIGN KEY("GraphicsCollection_id") REFERENCES "GraphicsCollection" (id),
	FOREIGN KEY(collection_id) REFERENCES graphic (id)
);CREATE INDEX "ix_GraphicsCollection_collection_collection_id" ON "GraphicsCollection_collection" (collection_id);CREATE INDEX "ix_GraphicsCollection_collection_GraphicsCollection_id" ON "GraphicsCollection_collection" ("GraphicsCollection_id");
CREATE TABLE "ModelParameters_input_format_map" (
	"ModelParameters_id" INTEGER,
	input_format_map_id INTEGER,
	PRIMARY KEY ("ModelParameters_id", input_format_map_id),
	FOREIGN KEY("ModelParameters_id") REFERENCES "ModelParameters" (id),
	FOREIGN KEY(input_format_map_id) REFERENCES "KeyVal" (id)
);CREATE INDEX "ix_ModelParameters_input_format_map_input_format_map_id" ON "ModelParameters_input_format_map" (input_format_map_id);CREATE INDEX "ix_ModelParameters_input_format_map_ModelParameters_id" ON "ModelParameters_input_format_map" ("ModelParameters_id");
CREATE TABLE "ModelParameters_output_format_map" (
	"ModelParameters_id" INTEGER,
	output_format_map_id INTEGER,
	PRIMARY KEY ("ModelParameters_id", output_format_map_id),
	FOREIGN KEY("ModelParameters_id") REFERENCES "ModelParameters" (id),
	FOREIGN KEY(output_format_map_id) REFERENCES "KeyVal" (id)
);CREATE INDEX "ix_ModelParameters_output_format_map_output_format_map_id" ON "ModelParameters_output_format_map" (output_format_map_id);CREATE INDEX "ix_ModelParameters_output_format_map_ModelParameters_id" ON "ModelParameters_output_format_map" ("ModelParameters_id");
CREATE TABLE "Considerations_users" (
	"Considerations_id" INTEGER,
	users_id INTEGER,
	PRIMARY KEY ("Considerations_id", users_id),
	FOREIGN KEY("Considerations_id") REFERENCES "Considerations" (id),
	FOREIGN KEY(users_id) REFERENCES "User" (id)
);CREATE INDEX "ix_Considerations_users_users_id" ON "Considerations_users" (users_id);CREATE INDEX "ix_Considerations_users_Considerations_id" ON "Considerations_users" ("Considerations_id");
CREATE TABLE "Considerations_use_cases" (
	"Considerations_id" INTEGER,
	use_cases_id INTEGER,
	PRIMARY KEY ("Considerations_id", use_cases_id),
	FOREIGN KEY("Considerations_id") REFERENCES "Considerations" (id),
	FOREIGN KEY(use_cases_id) REFERENCES "UseCase" (id)
);CREATE INDEX "ix_Considerations_use_cases_use_cases_id" ON "Considerations_use_cases" (use_cases_id);CREATE INDEX "ix_Considerations_use_cases_Considerations_id" ON "Considerations_use_cases" ("Considerations_id");
CREATE TABLE "Considerations_limitations" (
	"Considerations_id" INTEGER,
	limitations_id INTEGER,
	PRIMARY KEY ("Considerations_id", limitations_id),
	FOREIGN KEY("Considerations_id") REFERENCES "Considerations" (id),
	FOREIGN KEY(limitations_id) REFERENCES "Limitation" (id)
);CREATE INDEX "ix_Considerations_limitations_limitations_id" ON "Considerations_limitations" (limitations_id);CREATE INDEX "ix_Considerations_limitations_Considerations_id" ON "Considerations_limitations" ("Considerations_id");
CREATE TABLE "Considerations_tradeoffs" (
	"Considerations_id" INTEGER,
	tradeoffs_id INTEGER,
	PRIMARY KEY ("Considerations_id", tradeoffs_id),
	FOREIGN KEY("Considerations_id") REFERENCES "Considerations" (id),
	FOREIGN KEY(tradeoffs_id) REFERENCES "Tradeoff" (id)
);CREATE INDEX "ix_Considerations_tradeoffs_tradeoffs_id" ON "Considerations_tradeoffs" (tradeoffs_id);CREATE INDEX "ix_Considerations_tradeoffs_Considerations_id" ON "Considerations_tradeoffs" ("Considerations_id");
CREATE TABLE "Considerations_ethical_considerations" (
	"Considerations_id" INTEGER,
	ethical_considerations_id INTEGER,
	PRIMARY KEY ("Considerations_id", ethical_considerations_id),
	FOREIGN KEY("Considerations_id") REFERENCES "Considerations" (id),
	FOREIGN KEY(ethical_considerations_id) REFERENCES risk (id)
);CREATE INDEX "ix_Considerations_ethical_considerations_ethical_considerations_id" ON "Considerations_ethical_considerations" (ethical_considerations_id);CREATE INDEX "ix_Considerations_ethical_considerations_Considerations_id" ON "Considerations_ethical_considerations" ("Considerations_id");
CREATE TABLE "modelCard" (
	id INTEGER NOT NULL,
	schema_version TEXT,
	model_category TEXT,
	bias_model TEXT,
	bias_output TEXT,
	framework TEXT,
	framework_version TEXT,
	library_name TEXT,
	pipeline_tag TEXT,
	base_model TEXT,
	model_details_id INTEGER NOT NULL,
	model_parameters_id INTEGER,
	quantitative_analysis_id INTEGER,
	considerations_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(model_details_id) REFERENCES "ModelDetails" (id),
	FOREIGN KEY(model_parameters_id) REFERENCES "ModelParameters" (id),
	FOREIGN KEY(quantitative_analysis_id) REFERENCES "QuantitativeAnalysis" (id),
	FOREIGN KEY(considerations_id) REFERENCES "Considerations" (id)
);CREATE INDEX "ix_modelCard_id" ON "modelCard" (id);
CREATE TABLE "ModelDetails_owners" (
	"ModelDetails_id" INTEGER,
	owners_id INTEGER,
	PRIMARY KEY ("ModelDetails_id", owners_id),
	FOREIGN KEY("ModelDetails_id") REFERENCES "ModelDetails" (id),
	FOREIGN KEY(owners_id) REFERENCES owner (id)
);CREATE INDEX "ix_ModelDetails_owners_owners_id" ON "ModelDetails_owners" (owners_id);CREATE INDEX "ix_ModelDetails_owners_ModelDetails_id" ON "ModelDetails_owners" ("ModelDetails_id");
CREATE TABLE "ModelDetails_licenses" (
	"ModelDetails_id" INTEGER,
	licenses_id INTEGER,
	PRIMARY KEY ("ModelDetails_id", licenses_id),
	FOREIGN KEY("ModelDetails_id") REFERENCES "ModelDetails" (id),
	FOREIGN KEY(licenses_id) REFERENCES "License" (id)
);CREATE INDEX "ix_ModelDetails_licenses_licenses_id" ON "ModelDetails_licenses" (licenses_id);CREATE INDEX "ix_ModelDetails_licenses_ModelDetails_id" ON "ModelDetails_licenses" ("ModelDetails_id");
CREATE TABLE "ModelDetails_references" (
	"ModelDetails_id" INTEGER,
	references_id INTEGER,
	PRIMARY KEY ("ModelDetails_id", references_id),
	FOREIGN KEY("ModelDetails_id") REFERENCES "ModelDetails" (id),
	FOREIGN KEY(references_id) REFERENCES "Reference" (id)
);CREATE INDEX "ix_ModelDetails_references_references_id" ON "ModelDetails_references" (references_id);CREATE INDEX "ix_ModelDetails_references_ModelDetails_id" ON "ModelDetails_references" ("ModelDetails_id");
CREATE TABLE "ModelDetails_citations" (
	"ModelDetails_id" INTEGER,
	citations_id INTEGER,
	PRIMARY KEY ("ModelDetails_id", citations_id),
	FOREIGN KEY("ModelDetails_id") REFERENCES "ModelDetails" (id),
	FOREIGN KEY(citations_id) REFERENCES "Citation" (id)
);CREATE INDEX "ix_ModelDetails_citations_citations_id" ON "ModelDetails_citations" (citations_id);CREATE INDEX "ix_ModelDetails_citations_ModelDetails_id" ON "ModelDetails_citations" ("ModelDetails_id");
CREATE TABLE "ModelParameters_data" (
	"ModelParameters_id" INTEGER,
	data_id INTEGER,
	PRIMARY KEY ("ModelParameters_id", data_id),
	FOREIGN KEY("ModelParameters_id") REFERENCES "ModelParameters" (id),
	FOREIGN KEY(data_id) REFERENCES "dataSet" (id)
);CREATE INDEX "ix_ModelParameters_data_data_id" ON "ModelParameters_data" (data_id);CREATE INDEX "ix_ModelParameters_data_ModelParameters_id" ON "ModelParameters_data" ("ModelParameters_id");
CREATE TABLE "QuantitativeAnalysis_performance_metrics" (
	"QuantitativeAnalysis_id" INTEGER,
	performance_metrics_id INTEGER,
	PRIMARY KEY ("QuantitativeAnalysis_id", performance_metrics_id),
	FOREIGN KEY("QuantitativeAnalysis_id") REFERENCES "QuantitativeAnalysis" (id),
	FOREIGN KEY(performance_metrics_id) REFERENCES "performanceMetric" (id)
);CREATE INDEX "ix_QuantitativeAnalysis_performance_metrics_performance_metrics_id" ON "QuantitativeAnalysis_performance_metrics" (performance_metrics_id);CREATE INDEX "ix_QuantitativeAnalysis_performance_metrics_QuantitativeAnalysis_id" ON "QuantitativeAnalysis_performance_metrics" ("QuantitativeAnalysis_id");
CREATE TABLE "BenchmarkResult_metrics" (
	"BenchmarkResult_id" INTEGER,
	metrics_id INTEGER,
	PRIMARY KEY ("BenchmarkResult_id", metrics_id),
	FOREIGN KEY("BenchmarkResult_id") REFERENCES "BenchmarkResult" (id),
	FOREIGN KEY(metrics_id) REFERENCES "BenchmarkMetric" (id)
);CREATE INDEX "ix_BenchmarkResult_metrics_metrics_id" ON "BenchmarkResult_metrics" (metrics_id);CREATE INDEX "ix_BenchmarkResult_metrics_BenchmarkResult_id" ON "BenchmarkResult_metrics" ("BenchmarkResult_id");
CREATE TABLE "ModelIndex_results" (
	"ModelIndex_id" INTEGER,
	results_id INTEGER,
	PRIMARY KEY ("ModelIndex_id", results_id),
	FOREIGN KEY("ModelIndex_id") REFERENCES "ModelIndex" (id),
	FOREIGN KEY(results_id) REFERENCES "BenchmarkResult" (id)
);CREATE INDEX "ix_ModelIndex_results_results_id" ON "ModelIndex_results" (results_id);CREATE INDEX "ix_ModelIndex_results_ModelIndex_id" ON "ModelIndex_results" ("ModelIndex_id");
CREATE TABLE "modelCard_language" (
	"modelCard_id" INTEGER,
	language TEXT,
	PRIMARY KEY ("modelCard_id", language),
	FOREIGN KEY("modelCard_id") REFERENCES "modelCard" (id)
);CREATE INDEX "ix_modelCard_language_modelCard_id" ON "modelCard_language" ("modelCard_id");CREATE INDEX "ix_modelCard_language_language" ON "modelCard_language" (language);
CREATE TABLE "modelCard_tags" (
	"modelCard_id" INTEGER,
	tags TEXT,
	PRIMARY KEY ("modelCard_id", tags),
	FOREIGN KEY("modelCard_id") REFERENCES "modelCard" (id)
);CREATE INDEX "ix_modelCard_tags_modelCard_id" ON "modelCard_tags" ("modelCard_id");CREATE INDEX "ix_modelCard_tags_tags" ON "modelCard_tags" (tags);
CREATE TABLE "modelCard_datasets" (
	"modelCard_id" INTEGER,
	datasets TEXT,
	PRIMARY KEY ("modelCard_id", datasets),
	FOREIGN KEY("modelCard_id") REFERENCES "modelCard" (id)
);CREATE INDEX "ix_modelCard_datasets_datasets" ON "modelCard_datasets" (datasets);CREATE INDEX "ix_modelCard_datasets_modelCard_id" ON "modelCard_datasets" ("modelCard_id");
CREATE TABLE "modelCard_metrics" (
	"modelCard_id" INTEGER,
	metrics TEXT,
	PRIMARY KEY ("modelCard_id", metrics),
	FOREIGN KEY("modelCard_id") REFERENCES "modelCard" (id)
);CREATE INDEX "ix_modelCard_metrics_metrics" ON "modelCard_metrics" (metrics);CREATE INDEX "ix_modelCard_metrics_modelCard_id" ON "modelCard_metrics" ("modelCard_id");
CREATE TABLE "modelCard_model_index" (
	"modelCard_id" INTEGER,
	model_index_id INTEGER,
	PRIMARY KEY ("modelCard_id", model_index_id),
	FOREIGN KEY("modelCard_id") REFERENCES "modelCard" (id),
	FOREIGN KEY(model_index_id) REFERENCES "ModelIndex" (id)
);CREATE INDEX "ix_modelCard_model_index_model_index_id" ON "modelCard_model_index" (model_index_id);CREATE INDEX "ix_modelCard_model_index_modelCard_id" ON "modelCard_model_index" ("modelCard_id");
