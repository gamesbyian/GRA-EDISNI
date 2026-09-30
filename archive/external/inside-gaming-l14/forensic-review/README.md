# Inside Gaming L14 forensic review bundle

Source: Inside Gaming Collector's Edition unboxing, YouTube `AO2YQCl5qFM`.

Historical identity: lost sticker **L14**, visible symbol **`/`**, serial unknown.

This directory preserves the **exact JPEG files generated during the 2026-09-29 L14
recovery pass**. They are derived from source-video pixels and classical image processing
only. No generative AI, inpainting, synthetic super-resolution, or invented pixel detail
was used.

Methods represented include native-frame contact sheets, nearest/Lanczos enlargement,
channel separation, conservative contrast/sharpening, Richardson-Lucy deconvolution,
geometric normalization, adjacent-frame registration, and temporal stacking.

Result: the expected three-digit serial region is geometrically behind the presenter's
fingers throughout the useful sequence. Stable slash geometry is visible; stable numeral
strokes are not. Faint marks outside the expected number region are not evidence of digits.

The `clean324_simulated*.jpg` files are degradation/reference sanity checks using a known
sticker and are **not evidence about L14**.

Reproduction helper: `scripts/external_evidence/reproduce_l14_forensics.py`

## Exact files

- `all_right_edge.jpg` — Git blob `009d2627d15e9a350a0fd3f75a8ae3e35c1c5570`, 641278 bytes
- `clean324_simulated.jpg` — Git blob `cb0cc4d7302e940ab4044e10cd099d845eda19dc`, 144625 bytes
- `clean324_simulated2.jpg` — Git blob `f6bd35d301ecd76de75803a24d11e49c520a11c5`, 141654 bytes
- `clean324_simulated3.jpg` — Git blob `7e7918a706db3e7af330b37691808f264c650bf3`, 215944 bytes
- `deconv_frame109.jpg` — Git blob `867892a7c6aa5ecbc0c23818df684b950373be16`, 388759 bytes
- `early_sticker_frames.jpg` — Git blob `bf8364fbbb68ca68736ca81490ad411697ad50fe`, 1114431 bytes
- `frame109_channels.jpg` — Git blob `d0f76976ba4e3eb902822daf4d6a792d94f39ba1`, 512636 bytes
- `late_sticker_frames.jpg` — Git blob `656642812e8c381cb1a638e064fcc4f4925ef2fb`, 538134 bytes
- `rectified_stickers.jpg` — Git blob `5170c7222338fdbf465a82fd4b43f6c33c57d6db`, 110706 bytes
- `serial_expected_region.jpg` — Git blob `7a558e7b38648ee9aca876a946a7dc23b8a0ed26`, 322367 bytes
- `serial_occlusion_geometry.jpg` — Git blob `2c2d3e191c7079fd1c07fcf01e96acaf75bdab1a`, 259961 bytes
- `serial_strip_nearest.jpg` — Git blob `45ddb70937bf03c1cd23ee4628b3271df6716246`, 652042 bytes
- `sticker_all_native_contact.jpg` — Git blob `5544bca131b7e9dd6149e1c6e2270db43578b61b`, 1254261 bytes
- `sticker_enhanced_108_120.jpg` — Git blob `ff2ab3c8523fe51fd43e736b91dde4e80b8d3bde`, 425115 bytes
- `aligned_serial_stack.jpg` — Git blob `2d35437e020d1cd25a8dc1f2ce0856febadac931`, 266201 bytes
