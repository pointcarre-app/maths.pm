# Cubrick - SVG Animation Recorder



Record SVG animations with transparency for video editing.


> Frames were wrong because we clipped the page; I switched to element-level screenshots and bumped duration to 5 seconds at 30 fps. Each target is scrolled into view before capture.
I added stable anchors to the template so we can scroll reliably: #anchor-roll-once, #anchor-roll-twice, #anchor-roll-thrice on the three .js-rolling-container-* divs.
Conversion now uses ProRes 4444 with alpha (-profile:v 4 -pix_fmt yuva444p10le -alpha_bits 8). Yes, this preserves transparency in .mov.



## Setup
`npm install` 



## Quick record and convert
npm run capture
npm run convert-all

## Step by step
npm run serve        # Start server
npm run record       # Record frames
npm run convert-all  # Convert all three identity animations
npm run convert-green       # Convert with green screen




## Complete Setup
```bash
# Install dependencies
npm install

# Final structure check
tree



cd cubrick
npm run capture          # Records animation
npm run convert-all  # Creates 3 MOVs with alpha in output/
```