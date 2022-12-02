
# 🚦 Validation Reports

This site is a central place for you to view the validation results for the
ingest package you're developing in your [Pull Request](https://github.com/znatty22/d3b-ingest-packages/pull/5).

Each time you push a commit to your PR, the Github workflow will do the following:

1. Kick off a dry run ingest (`kidsfirst test <path/to/your/package>`)
2. Run validation on the output data from both the Extract Stage and Transform
   Stage of your ingest
3. Build a validation report for each stage's output data

You can view those validation reports below

## Ingest Package - SD_ME0WME0W

- [ExtractStage Report](results/ExtractStage/validation_results.md)
- [TransformStage Report](results/TransformStage/validation_results.md)
