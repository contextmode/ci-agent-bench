# Judge file r2-transformers-5.20.1

## PUBLISHED RELEASE NOTES (written by the maintainers)

# Release v5.20.1

Special surprise including the new model Beam from Reflection AI :partying_face: 

<img width="2912" height="1440" alt="Gemini_Generated_Image_ox4hjlox4hjlox4h" src="https://github.com/user-attachments/assets/bfc7ff16-4340-490c-925c-b1512e4ceb32" />

Beam is a token-efficient, frontier-scale model focused on coding and agentic use cases. It is built for teams that want to run a powerful model on their own hardware, infrastructure, or cloud, and customize it to their specific needs.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/beam)
* Fix small bug in auto mappings (#49664) by @yonigozlan in [#49664](https://github.com/huggingface/transformers/pull/49664)


## Some real patch fixes

We broke loading models on older torch versions :cry: should be fixed now. But here is the full list of fixes

- Fix HunYuan-VL image assignment during batched generation (#49557) by @Arnav66692
- Fix DeepGEMM Mega MoE under expert parallelism(#49428) by @IlyasMoutawwakil
- Fix from_pretrained on torch 2.7: require torch>=2.8 for distributed checkpointing (#49652) by @naveecode 
- Make DtensorShardOperation work on torch 2.6 and 2.7 (#49657) by @hazelxue

**Full Changelog**: https://github.com/huggingface/transformers/compare/v5.20.0...v5.20.1

## COMMIT SUBJECTS between the previous tag and the release

Fix HunYuan-VL image assignment during batched generation (#49557)
Fix DeepGEMM Mega MoE under expert parallelism (#49428)
Fix from_pretrained on torch 2.7: require torch>=2.8 for distributed checkpointing (#49652)
Make `DtensorShardOperation` work on torch 2.6 and 2.7 (#49657)
Fix small bug in auto mappings (#49664)
v5.20.1

# CANDIDATE A

## Patch release v5.20.1

This patch adds the Beam model and fixes batched generation for HunYuan-VL, DeepGEMM Mega MoE under expert parallelism, and distributed loading on older PyTorch versions.

### New model

- Add the Beam model (a mixture-of-experts causal language model from Reflection AI), with `BeamConfig` and Auto class support. ([#49664](https://github.com/huggingface/transformers/pull/49664))

### Bug fixes

- Fix HunYuan-VL giving the wrong image to some sequences during batched generation, such as beam search. Image features are now returned per image. ([#49557](https://github.com/huggingface/transformers/pull/49557))
- The same per-image feature fix applies to Idefics2, Idefics3, SmolVLM, LlavaNextVideo and ModernVBert. ([#49557](https://github.com/huggingface/transformers/pull/49557))
- Fix DeepGEMM Mega MoE crashing on the first forward pass when run with expert parallelism (`tp_size=ep_size`), as with DeepSeek-V4. ([#49428](https://github.com/huggingface/transformers/pull/49428))
- Fix `from_pretrained` failing on torch 2.7 by requiring torch>=2.8 for distributed checkpointing, with clearer error messages. ([#49652](https://github.com/huggingface/transformers/pull/49652))
- Fix tensor-parallel loading raising `AttributeError` on torch 2.6 and 2.7. ([#49657](https://github.com/huggingface/transformers/pull/49657))

### Breaking changes

- Distributed checkpointing (`hf_storage`) and the FSDP2/DCP path now require torch>=2.8. ([#49652](https://github.com/huggingface/transformers/pull/49652))
- Mega MoE now requires `ep_size == tp_size` when used with expert parallelism. ([#49428](https://github.com/huggingface/transformers/pull/49428))

### Other

- Add tests for Beam, shared multimodal `pooler_output` checks, chat parsing, and FP8, and update the version to 5.20.1. ([#49664](https://github.com/huggingface/transformers/pull/49664), [#49557](https://github.com/huggingface/transformers/pull/49557))


# CANDIDATE B

# Transformers v5.20.1

Patch release with a new model, Beam, plus fixes for torch 2.6/2.7 compatibility, expert parallelism, and batched HunYuan-VL generation.

## New model

- **Beam** from Reflection AI: a text-only sparse mixture-of-experts language model (501B total parameters, 23B active per token) for coding, reasoning, and agentic work. It is available through `AutoModelForCausalLM` and has a docs page. It also adds chat response parsing tests. ([#49664](https://github.com/huggingface/transformers/pull/49664))

## Bug fixes

- Fixed `from_pretrained` failing on torch 2.7 with `ModuleNotFoundError` for `torch.distributed.checkpoint.hf_storage`. Distributed checkpointing and the FSDP2 checks now require torch 2.8 or newer, and the error messages say so. ([#49652](https://github.com/huggingface/transformers/pull/49652))
- Fixed tensor-parallel loading on torch 2.6 and 2.7, which raised `AttributeError` about `local_shard_size_and_offset`. ([#49657](https://github.com/huggingface/transformers/pull/49657))
- Fixed DeepGEMM Mega MoE under expert parallelism, where the first forward pass raised an error. Mega MoE now takes over the experts sharding rule, runs on the tensor-parallel group, and requires `ep_size == tp_size`. ([#49428](https://github.com/huggingface/transformers/pull/49428))
- Fixed HunYuan-VL giving some beams the wrong image during batched generation. Image features are now split per image. ([#49557](https://github.com/huggingface/transformers/pull/49557))
- Fixed the same image-feature shape handling in the Idefics2, Idefics3, SmolVLM, ModernVBert and LLaVA-NeXT-Video models, which changed alongside the HunYuan-VL fix. ([#49557](https://github.com/huggingface/transformers/pull/49557))

## Other

- Added tests for the distributed checkpoint guard, sharding utilities, HunYuan-VL beam search and chat parsing, and moved the shared `pooler_output` test into its own test. ([#49652](https://github.com/huggingface/transformers/pull/49652), [#49557](https://github.com/huggingface/transformers/pull/49557), [#49664](https://github.com/huggingface/transformers/pull/49664))

