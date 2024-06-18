#!/usr/bin/env python3
"""Tool to run a single Resource class scan. Useful during developing Resource classes
and their Schemas. Run without usage for details."""

import sys
from typing import List, Optional

from resource_graph.server.resource_extractor import ResourceExtractor


def main() -> int:
    extractor = ResourceExtractor()
    exception, path = extractor.start_scanner(regions=["us-east-1"])
    extractor.read_xml_blocks(path, "4510",False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
