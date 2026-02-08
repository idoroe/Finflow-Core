using Finflow.Core.Pipeline;

// Get the project root directory (3 levels up from bin/Debug/net10.0)
var projectRoot = Path.GetFullPath(Path.Combine(AppContext.BaseDirectory, "..", "..", "..", "..", ".."));
var rawDataPath = Path.Combine(projectRoot, "data", "raw");
var analyticsOutputPath = Path.Combine(projectRoot, "data", "analytics");

// Run the data pipeline
var pipeline = new DataPipeline(rawDataPath, analyticsOutputPath);
pipeline.Run();
