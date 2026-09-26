# Order Book Visualization

An interactive browser-based viewer for order book snapshots and trade events stored in Apache Feather files. It supports multiple products and trading dates, synchronized timelines, intraday navigation, zooming, adjacent-snapshot comparison, and a filterable trade log.

## Requirements

- Python 3
- A modern desktop browser
- Internet access when the page starts, because D3, Apache Arrow, LZ4, and Zstandard are loaded from CDNs

## Start the Viewer

### Windows

Double-click `start_windows.bat`.

### macOS

Double-click `start_mac.command`.

If macOS blocks the script, right-click `start_mac.command` and select **Open**.

### Linux

Open a terminal in this directory and run:

```bash
python3 start_server.py
```

The startup script runs a local HTTP server and opens the viewer in your default browser. Keep the terminal window open while using the viewer. Press `Ctrl+C` in the terminal to stop the server.

To start the server without opening a browser, or to request a different port, run:

```bash
python3 start_server.py --no-browser --port 8000
```

If the requested port is already in use, the server automatically selects an available port.

## Data Layout

Store market-data and trade files in matching date folders:

```text
data/
└── YYYY/
    └── MM/
        └── DD/
            ├── md/
            │   └── PRODUCT.feather
            └── trade/
                └── PRODUCT.feather
```

For example:

```text
data/2026/04/16/md/AU2606-SH.feather
data/2026/04/16/trade/AU2606-SH.feather
```

A product is available only when identically named Feather files exist in both the `md` and `trade` folders. Dates and products are discovered each time the server starts. Product names are inferred from file names, so adding a product only requires adding the matching pair of files; no HTML changes are needed.

## Expected Columns

Market-data files must contain:

- A timestamp column named `dt`, `dt_lc`, or `dt_exch`
- A last-price column named `price` or `last_px`
- Best-bid and best-ask price columns named `b1p`/`a1p` or `bid1_px`/`ask1_px`

Trade files must contain:

- A contract column named `contract`, `symbol`, or `instrument`
- A timestamp column named `dt`, `dt_lc`, or `dt_exch`
- An instruction column named `instruction`, `instr`, or `order_instruction`
- A trade-price column named `price_trd`, `trade_price`, or `last_trd`

When level-two through level-five prices and quantities are present, the snapshot cards display five order book levels. Otherwise, they display the best bid and ask only.

## Loading Data

After the viewer scans the local `data` directory, choose one or more date folders and click **Load Selected Folders**. You can add folders one at a time, remove individual selections, or clear the list.

The viewer also supports selecting individual `md` Feather files when it is running through `start_server.py`; the matching trade files are then loaded automatically from the discovered data layout.

Use **Choose Folders** at any time to load a different set of data. If files are added while the server is already running, refresh the page to rescan the `data` directory.

## Main Controls

- **Main Chart Dates** selects one or more loaded trading dates for the combined chart.
- **Go to Date** and **View Full Day** navigate to one complete trading date.
- The intraday time controls zoom to a specific range. Daytime and overnight ranges such as `21:00:00` to `02:00:00` are supported.
- Scroll over the chart to zoom. Drag to pan. Press `R` to reset the view.
- Click a product title to enlarge that product's panel; click it again to restore all panels.
- Drag product titles to reorder the panels. The order is saved in browser storage.
- Hover over the chart to inspect synchronized snapshots. Click to pin or unpin the current point.
- Click a snapshot card to compare the `-2`, `-1`, `0`, `+1`, and `+2` neighboring snapshots.
- Filter the trade log by product. Double-click a trade to locate it on the main chart.
- Click the trade-log heading to expand or collapse the log. Press `Escape` to close the expanded view.
- Use **Font Size** to scale the detail panel text.

## Notes

- Feather timestamps are displayed with nanosecond precision when available.
- Large inactive gaps in the timeline are compressed to keep active trading periods readable.
- The viewer recognizes both English instruction keys such as `open_long` and the Chinese instruction values used by the included datasets, but all interface labels are displayed in English.
