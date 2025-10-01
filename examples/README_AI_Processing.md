# AI-Powered Processing with Panparsex

Panparsex now includes AI-powered post-processing capabilities using OpenAI GPT models. This allows you to analyze, restructure, and filter parsed content intelligently.

## Features

- **Intelligent Analysis**: Use GPT to understand and analyze parsed content
- **Content Restructuring**: Reorganize information in logical, coherent ways
- **Smart Filtering**: Remove irrelevant information and highlight key points
- **Multiple Output Formats**: JSON, Markdown, or plain text summaries
- **Customizable Tasks**: Define specific analysis tasks for your use case

## Installation

Make sure you have panparsex installed with AI support:

```bash
pip install panparsex
```

## Setup

1. Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Set the API key as an environment variable:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

Or pass it directly in your code:

```python
from panparsex.ai_processor import AIProcessor
processor = AIProcessor(api_key="your-api-key-here")
```

## Usage

### Command Line Interface

#### Basic AI Processing

```bash
# Parse a PDF and process with AI
panparsex parse document.pdf --ai-process --ai-output analysis.json

# Parse a website and get a markdown summary
panparsex parse https://example.com --ai-process --ai-format markdown --ai-output summary.md

# Parse a text file with custom task
panparsex parse report.txt --ai-process --ai-task "Extract key metrics and recommendations" --ai-format structured_json
```

#### Advanced Options

```bash
# Use a specific GPT model
panparsex parse document.pdf --ai-process --ai-model gpt-4o --ai-tokens 8000

# Adjust creativity (temperature)
panparsex parse document.pdf --ai-process --ai-temperature 0.7

# Custom output file
panparsex parse document.pdf --ai-process --ai-output custom_analysis.json
```

### Python API

#### Basic Usage

```python
from panparsex import parse
from panparsex.ai_processor import AIProcessor

# Parse a document
doc = parse("document.pdf")

# Process with AI
processor = AIProcessor(api_key="your-api-key")
result = processor.process_and_save(
    doc,
    "analysis.json",
    task="Analyze and restructure the content",
    output_format="structured_json"
)
```

#### Advanced Usage

```python
from panparsex import parse
from panparsex.ai_processor import AIProcessor

# Parse a website
doc = parse("https://example.com", recursive=True, max_links=10)

# Process with AI for content analysis
processor = AIProcessor(
    api_key="your-api-key",
    model="gpt-4o-mini"
)

result = processor.process_and_save(
    doc,
    "website_analysis.md",
    task="Extract key information, identify main topics, and create a structured summary",
    output_format="markdown",
    max_tokens=4000,
    temperature=0.3
)
```

## Output Formats

### Structured JSON

Returns a structured JSON object with:

```json
{
  "summary": "Brief overview of the content",
  "key_topics": ["topic1", "topic2", "topic3"],
  "important_points": ["point1", "point2", "point3"],
  "structured_content": {
    "section1": "content",
    "section2": "content"
  },
  "insights": ["insight1", "insight2"],
  "recommendations": ["recommendation1", "recommendation2"]
}
```

### Markdown

Returns well-formatted markdown with headers, lists, and proper structure.

### Summary

Returns a concise text summary of the key points.

## Use Cases

### 1. Document Analysis

```python
# Analyze a business report
result = processor.process_and_save(
    doc,
    "business_analysis.json",
    task="Extract key metrics, identify challenges, and provide recommendations",
    output_format="structured_json"
)
```

### 2. Content Summarization

```python
# Summarize a long article
result = processor.process_and_save(
    doc,
    "summary.md",
    task="Create a concise summary highlighting the main points",
    output_format="markdown"
)
```

### 3. Technical Documentation Processing

```python
# Process API documentation
result = processor.process_and_save(
    doc,
    "api_guide.json",
    task="Extract endpoints, authentication methods, and usage examples",
    output_format="structured_json"
)
```

### 4. Research Paper Analysis

```python
# Analyze a research paper
result = processor.process_and_save(
    doc,
    "research_analysis.json",
    task="Extract key findings, methodology, and conclusions",
    output_format="structured_json"
)
```

### 5. Website Content Extraction

```python
# Extract structured information from a website
result = processor.process_and_save(
    doc,
    "website_data.json",
    task="Extract contact information, services, and key features",
    output_format="structured_json"
)
```

## Configuration Options

### AI Models

- `gpt-4o-mini` (default): Fast and cost-effective
- `gpt-4o`: More capable but slower and more expensive
- `gpt-3.5-turbo`: Legacy model, still available

### Parameters

- `max_tokens`: Maximum tokens for the response (default: 4000)
- `temperature`: Controls randomness (0.0-1.0, default: 0.3)
- `task`: Description of what you want the AI to do
- `output_format`: Format of the output (structured_json, markdown, summary)

## Examples

See `examples/ai_processing_example.py` for comprehensive examples of:

- PDF processing and analysis
- Website content extraction
- Business report analysis
- Technical documentation processing
- Custom AI tasks

## Error Handling

The AI processor includes robust error handling:

- Falls back gracefully if AI processing fails
- Provides clear error messages
- Continues with original parsing if AI is unavailable

## Best Practices

1. **Start with simple tasks**: Begin with basic analysis and gradually add complexity
2. **Use appropriate models**: Choose the right model for your needs and budget
3. **Set reasonable token limits**: Avoid excessive token usage
4. **Test with small documents**: Validate your setup with small files first
5. **Monitor API usage**: Keep track of your OpenAI API usage and costs

## Troubleshooting

### Common Issues

1. **API Key Error**: Make sure your OpenAI API key is set correctly
2. **Rate Limits**: OpenAI has rate limits, consider adding delays between requests
3. **Token Limits**: Large documents may exceed token limits, consider chunking
4. **Model Availability**: Some models may not be available in all regions

### Getting Help

- Check the [OpenAI API Documentation](https://platform.openai.com/docs)
- Review the [panparsex GitHub Issues](https://github.com/dhruvildarji/panparser/issues)
- Join the [panparsex Discussions](https://github.com/dhruvildarji/panparser/discussions)

## Cost Considerations

AI processing uses OpenAI's API, which has costs based on:

- Model used (gpt-4o is more expensive than gpt-4o-mini)
- Number of tokens processed
- Number of requests made

Monitor your usage at [OpenAI Usage Dashboard](https://platform.openai.com/usage).
