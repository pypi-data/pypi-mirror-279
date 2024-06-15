# Description

Space related R&D

# Initialize the server

```
python -m cosmic_counsel -d /data
```

# Ask questions
Cosmic Counsel reads questions from a file, usually called 'question.json.' It then outputs the response to the query, along with the timestamp, to a file called 'output.json.'

```bash
cosmic-counsel -q ./path/to/question.json -o ./path/to/output.json
```
