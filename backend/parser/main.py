"""
Entry point for the parser. Always run from here, so python understands project structure.

1. Accept files to ingest in the frontend.
2. Send to backend. Keep track of file names.
3. Save those files in directory.
4. Run extract info and ingestion process for only those files.

"""

from vdb.ingest import ingest_resumes

ingest_resumes()
