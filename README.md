# AI-Assisted Coding Interview: Couchbase Bulk Migration

## Scenario

We are upgrading our backend and need to migrate 100,000 user profile JSON
documents from an old local system into a Couchbase database. You will be
using an AI coding assistant (GitHub Copilot, ChatGPT, Claude, etc.) to write
the code.

## Goal

Your task is not just to generate code, but to guide the AI to write a
highly efficient, resilient script. You may use Python, Node.js, or Java.
You must ensure the AI doesn't just write a naive loop, but implements a
proper bulk-loading strategy.

You'll be evaluated on how you *direct* the AI (the prompts you give it, how
you push back on naive solutions, how you verify its output) — not just on
the final code.

## Setup

- Sample data lives in `sample_data/`. Run `sample_data/generate_sample_data.py`
  to (re)generate the full 100,000-document set as `sample_data/profiles/`.
  A handful of pre-generated example files are already included so you can
  inspect the schema without running anything.
- Pick your language and use the matching dependency file:
  - Node.js → `package.json` (Couchbase Node SDK)
  - Python → `requirements.txt` (Couchbase Python SDK)
  - Java → add your own `pom.xml`/`build.gradle` with the Couchbase Java SDK
- Put your implementation in `src/`, your tests in `tests/`.
- You do not need a real Couchbase cluster — mock the SDK for tests, and
  feel free to point at Couchbase Capella's free tier or a local Docker
  instance if you want to test against something real.

## Task

### Step 1: Read and Parse the Data

Prompt the AI to write a function that reads the legacy JSON files.

- **Requirement:** The script needs to read a large local JSON file (or a
  directory of JSON files) without running out of memory.
- **Ask the AI for:** a memory-efficient way to read large JSON datasets
  (streaming or chunking, not `JSON.parse`/`json.load` on the whole file).

### Step 2: Design the Async Batching Logic

Prompt the AI to create a bulk-insert function for Couchbase.

- **Requirement:** Inserting 100,000 documents one by one is too slow.
  Inserting all 100,000 at exactly the same time will crash the system.
- **Ask the AI for:** asynchronous batching (e.g., chunks of 500–1,000
  documents) using the official Couchbase SDK's bulk/concurrent APIs.

### Step 3: Add Resilience and Error Handling

Prompt the AI to handle inevitable network hiccups.

- **Requirement:** If the database drops the connection on document
  #45,000, the script shouldn't crash and lose its progress.
- **Ask the AI for:** a retry mechanism with exponential backoff for failed
  inserts, and a "dead-letter" file that logs documents which ultimately
  failed so they can be reviewed later.

### Step 4: Write the Tests

Prompt the AI to generate unit tests to prove the logic works.

- **Requirement:** We need to know the batching and retry logic actually
  works before running it on production data.
- **Ask the AI for:** tests using a mocked Couchbase collection/cluster that
  specifically verify (a) documents are grouped into batches correctly and
  (b) the script retries when a mock error is thrown.

## Deliverable

Push your code, tests, and a short `NOTES.md` describing the prompts you
used and any naive AI output you had to correct.
