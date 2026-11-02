# PR diff (the real change)

```diff
diff --git a/ggml/src/ggml-vulkan/ggml-vulkan-types.h b/ggml/src/ggml-vulkan/ggml-vulkan-types.h
index ee50f51a383..1aafe6399c6 100644
--- a/ggml/src/ggml-vulkan/ggml-vulkan-types.h
+++ b/ggml/src/ggml-vulkan/ggml-vulkan-types.h
@@ -855,8 +855,8 @@ struct vk_device_struct {
     vk_pipeline pipeline_roll_f32;
     vk_pipeline pipeline_repeat_i32, pipeline_repeat_back_f32;
     vk_pipeline pipeline_repeat_i16;
-    vk_pipeline pipeline_cpy_f32_f32, pipeline_cpy_f32_f16, pipeline_cpy_f16_f16, pipeline_cpy_f16_f32, pipeline_cpy_f32_bf16, pipeline_cpy_bf16_f32, pipeline_cpy_f32_i32, pipeline_cpy_i32_f32;
-    vk_pipeline pipeline_contig_cpy_f32_f32, pipeline_contig_cpy_f32_f16, pipeline_contig_cpy_f16_f16, pipeline_contig_cpy_f16_f32, pipeline_contig_cpy_f32_bf16, pipeline_contig_cpy_bf16_f32, pipeline_contig_cpy_f32_i32, pipeline_contig_cpy_i32_f32;
+    vk_pipeline pipeline_cpy_f32_f32, pipeline_cpy_f32_f16, pipeline_cpy_f16_f16, pipeline_cpy_f16_f32, pipeline_cpy_f32_bf16, pipeline_cpy_bf16_f32, pipeline_cpy_bf16_f16, pipeline_cpy_f32_i32, pipeline_cpy_i32_f32;
+    vk_pipeline pipeline_contig_cpy_f32_f32, pipeline_contig_cpy_f32_f16, pipeline_contig_cpy_f16_f16, pipeline_contig_cpy_f16_f32, pipeline_contig_cpy_f32_bf16, pipeline_contig_cpy_bf16_f32, pipeline_contig_cpy_bf16_f16, pipeline_contig_cpy_f32_i32, pipeline_contig_cpy_i32_f32;
     vk_pipeline pipeline_cpy_f32_quant[GGML_TYPE_COUNT];
     vk_pipeline pipeline_cpy_quant_f32[GGML_TYPE_COUNT];
     vk_pipeline pipeline_cpy_transpose_16, pipeline_cpy_transpose_32;
diff --git a/ggml/src/ggml-vulkan/ggml-vulkan.cpp b/ggml/src/ggml-vulkan/ggml-vulkan.cpp
index cbd3697ef9b..8d273ba3dd5 100644
--- a/ggml/src/ggml-vulkan/ggml-vulkan.cpp
+++ b/ggml/src/ggml-vulkan/ggml-vulkan.cpp
@@ -3277,6 +3277,7 @@ void ggml_vk_load_shaders(vk_device& device, vk_pipeline requested) {
     ggml_vk_create_pipeline(device, device->pipeline_cpy_f16_f32, "cpy_f16_f32", cpy_f16_f32_len, cpy_f16_f32_data, "main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_cpy_f32_bf16,"cpy_f32_bf16",cpy_f32_bf16_len,cpy_f32_bf16_data,"main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_cpy_bf16_f32,"cpy_bf16_f32",cpy_bf16_f32_len,cpy_bf16_f32_data,"main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
+    ggml_vk_create_pipeline(device, device->pipeline_cpy_bf16_f16,"cpy_bf16_f16",cpy_bf16_f16_len,cpy_bf16_f16_data,"main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_cpy_i32_f32, "cpy_i32_f32", cpy_i32_f32_len, cpy_i32_f32_data, "main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_cpy_f32_i32, "cpy_f32_i32", cpy_f32_i32_len, cpy_f32_i32_data, "main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
 
@@ -3286,6 +3287,7 @@ void ggml_vk_load_shaders(vk_device& device, vk_pipeline requested) {
     ggml_vk_create_pipeline(device, device->pipeline_contig_cpy_f16_f32, "contig_cpy_f16_f32", contig_cpy_f16_f32_len, contig_cpy_f16_f32_data, "main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_contig_cpy_f32_bf16,"contig_cpy_f32_bf16",contig_cpy_f32_bf16_len,contig_cpy_f32_bf16_data,"main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_contig_cpy_bf16_f32,"contig_cpy_bf16_f32",contig_cpy_bf16_f32_len,contig_cpy_bf16_f32_data,"main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
+    ggml_vk_create_pipeline(device, device->pipeline_contig_cpy_bf16_f16,"contig_cpy_bf16_f16",contig_cpy_bf16_f16_len,contig_cpy_bf16_f16_data,"main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_contig_cpy_i32_f32, "contig_cpy_i32_f32", contig_cpy_i32_f32_len, contig_cpy_i32_f32_data, "main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
     ggml_vk_create_pipeline(device, device->pipeline_contig_cpy_f32_i32, "contig_cpy_f32_i32", contig_cpy_f32_i32_len, contig_cpy_f32_i32_data, "main", 2, sizeof(vk_op_unary_push_constants), {512, 1, 1}, {}, 1);
 
@@ -6089,6 +6091,13 @@ vk_pipeline ggml_vk_get_cpy_pipeline(ggml_backend_vk_context * ctx, const ggml_t
             return ctx->device->pipeline_cpy_bf16_f32;
         }
     }
+    if (src->type == GGML_TYPE_BF16 && to == GGML_TYPE_F16) {
+        if (contig) {
+            return ctx->device->pipeline_contig_cpy_bf16_f16;
+        } else {
+            return ctx->device->pipeline_cpy_bf16_f16;
+        }
+    }
     if (src->type == GGML_TYPE_F32 && to == GGML_TYPE_I32) {
         if (contig) {
             return ctx->device->pipeline_contig_cpy_f32_i32;
@@ -6256,6 +6265,20 @@ static vk_pipeline ggml_vk_get_64b_indexing_pipeline(ggml_backend_vk_context * c
     return pipeline;
 }
 
+// perf-heuristic for choosing mul_mat b type, based on shader availability
+static ggml_type ggml_vk_mul_mat_b_type(
+        ggml_backend_vk_context * ctx, ggml_type src0_type, const ggml_tensor * src1,
+        ggml_type f16_type, ggml_prec prec, bool mul_mat_id, bool can_quantize_y, bool prefer_f16_b) {
+    auto available = [&](ggml_type b) {
+        return ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0_type, b, prec, mul_mat_id) != nullptr;
+    };
+    if (can_quantize_y && available(GGML_TYPE_Q8_1))             return GGML_TYPE_Q8_1;
+    if (prefer_f16_b   && available(f16_type))                   return f16_type;
+    if (ggml_vk_dim01_contiguous(src1) && available(src1->type)) return src1->type;
+    if (src1->type == GGML_TYPE_BF16 && available(GGML_TYPE_F32)) return GGML_TYPE_F32;
+    return f16_type;
+}
+
 static void ggml_vk_mul_mat_q_f16(ggml_backend_vk_context * ctx, vk_context& subctx, const ggml_tensor * src0, const ggml_tensor * src1, ggml_tensor * dst, bool disable_split_k) {
     VK_LOG_DEBUG("ggml_vk_mul_mat_q_f16((" << src0 << ", name=" << src0->name << ", type=" << ggml_type_name(src0->type) << ", ne0=" << src0->ne[0] << ", ne1=" << src0->ne[1] << ", ne2=" << src0->ne[2] << ", ne3=" << src0->ne[3] << ", nb0=" << src0->nb[0] << ", nb1=" << src0->nb[1] << ", nb2=" << src0->nb[2] << ", nb3=" << src0->nb[3];
     std::cerr << "), (" << src1 << ", name=" << src1->name << ", type=" << ggml_type_name(src1->type) << ", ne0=" << src1->ne[0] << ", ne1=" << src1->ne[1] << ", ne2=" << src1->ne[2] << ", ne3=" << src1->ne[3] << ", nb0=" << src1->nb[0] << ", nb1=" << src1->nb[1] << ", nb2=" << src1->nb[2] << ", nb3=" << src1->nb[3];
@@ -6300,51 +6323,35 @@ static void ggml_vk_mul_mat_q_f16(ggml_backend_vk_context * ctx, vk_context& sub
         src1_uma = d_Qy != nullptr;
     }
 
-    // TODO: Clean up this logic to pick src1 type by capability
-    // Reformat and convert to fp16 if non-contiguous, or for coopmat2 for better perf
     const bool x_non_contig = (ctx->device->coopmat2 && src0->type == GGML_TYPE_F32) ||
                               !ggml_vk_dim01_contiguous(src0);
     // If src0 is BF16, try to use a BF16 x BF16 multiply
     ggml_type f16_type = src0->type == GGML_TYPE_BF16 ? GGML_TYPE_BF16 : GGML_TYPE_F16;
 
-    // Prefer the int8 MMQ path (quantize src1 to q8_1) whenever a matching pipeline exists.
-    // The pipeline lookup returns nullptr for types without a q8_1 pipeline (e.g. RDNA4-skipped
-    // quants), in which case coopmat1 falls back to the f16 B-type quant matmul below.
-    bool quantize_y = (ctx->device->integer_dot_product || ctx->device->coopmat_int_support) &&
-                      src1->type == GGML_TYPE_F32 && ggml_is_contiguous(src1) && (ne11 * ne10) % 4 == 0;
+    const bool is_coopmat = ctx->device->coopmat_support || ctx->device->coopmat2;
+    const bool can_quantize_y = (ctx->device->integer_dot_product || ctx->device->coopmat_int_support) &&
+                                src1->type == GGML_TYPE_F32 && ggml_is_contiguous(src1) && (ne11 * ne10) % 4 == 0;
+    // coopmat shaders are fast enough that memory bandwidth reduction from f16 activations helps
+    const bool prefer_f16_b = is_coopmat && ggml_is_quantized(src0->type) && src1->type == GGML_TYPE_F32;
 
-    // Check for mmq first
-    const std::vector<vk_matmul_pipeline_pair>* mmp_map = quantize_y ? ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0->type, GGML_TYPE_Q8_1, (ggml_prec)dst->op_params[0]) : nullptr;
-    if (mmp_map == nullptr) {
-        quantize_y = false;
-    }
+    const ggml_type y_kernel_type = ggml_vk_mul_mat_b_type(ctx, src0->type, src1, f16_type,
+                                        (ggml_prec)dst->op_params[0], false, can_quantize_y, prefer_f16_b);
 
-    const bool y_non_contig = (ctx->device->coopmat2 && src1->type == GGML_TYPE_F32) ||
-                              // coopmat1: force f32->f16 conversion so the f16 B-type quant pipeline is
-                              // used, but only when the int8 MMQ path above is not taken.
-                              (ctx->device->coopmat_support && !ctx->device->coopmat2 && !quantize_y &&
-                               ggml_is_quantized(src0->type) && src1->type == GGML_TYPE_F32) ||
-                              (src0->type == GGML_TYPE_BF16 && src1->type != GGML_TYPE_BF16) ||
-                              !ggml_vk_dim01_contiguous(src1);
+    const bool quantize_y       = y_kernel_type == GGML_TYPE_Q8_1;
+    const bool y_f32_kernel     = y_kernel_type == GGML_TYPE_F32;
+    const bool y_needs_reformat = !quantize_y && (!ggml_vk_dim01_contiguous(src1) || y_kernel_type != src1->type);
 
-    const bool y_f32_kernel = src1->type == GGML_TYPE_F32 && !y_non_contig;
-
-    if (mmp_map == nullptr) {
-        // Fall back to f16 dequant mul mat
-        mmp_map = ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0->type, y_non_contig ? f16_type : src1->type, (ggml_prec)dst->op_params[0]);
-    }
+    const std::vector<vk_matmul_pipeline_pair>* mmp_map =
+        ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0->type, y_kernel_type, (ggml_prec)dst->op_params[0]);
 
     const bool qx_needs_dequant = mmp_map == nullptr || x_non_contig;
-    const bool qy_needs_dequant = !quantize_y && ((src1->type != f16_type && !y_f32_kernel) || y_non_contig);
+    const bool qy_needs_dequant = y_needs_reformat;
 
     if (qx_needs_dequant) {
-        // Fall back to dequant + f16 mulmat
-        mmp_map = ggml_vk_get_mul_mat_mat_pipeline_map(ctx, f16_type, y_f32_kernel ? GGML_TYPE_F32 : f16_type, (ggml_prec)dst->op_params[0]);
+        // dequant src0 to f16
+        mmp_map = ggml_vk_get_mul_mat_mat_pipeline_map(ctx, f16_type, y_kernel_type, (ggml_prec)dst->op_params[0]);
     }
 
-    // Not implemented
-    GGML_ASSERT(y_non_contig || !qy_needs_dequant);  // NOLINT
-
     GGML_ASSERT(mmp_map != nullptr);
 
     const uint32_t kpad = quantize_y ? 0 : ggml_vk_align_size(ne10, ggml_vk_guess_matmul_pipeline_align_map(ctx, *mmp_map, ne01, ne11, false));
@@ -6380,8 +6387,8 @@ static void ggml_vk_mul_mat_q_f16(ggml_backend_vk_context * ctx, vk_context& sub
     } else {
         to_fp16_vk_0 = ggml_vk_get_to_fp16(ctx, src0->type);
     }
-    if (y_non_contig) {
-        to_fp16_vk_1 = ggml_vk_get_cpy_pipeline(ctx, src1, nullptr, f16_type);
+    if (y_needs_reformat) {
+        to_fp16_vk_1 = ggml_vk_get_cpy_pipeline(ctx, src1, nullptr, y_kernel_type);
     } else {
         to_fp16_vk_1 = ggml_vk_get_to_fp16(ctx, src1->type);
     }
@@ -6479,7 +6486,7 @@ static void ggml_vk_mul_mat_q_f16(ggml_backend_vk_context * ctx, vk_context& sub
         ggml_vk_dispatch_pipeline(ctx, subctx, to_fp16_vk_0, { vk_subbuffer{ d_Qx, qx_buf_offset, qx_sz }, vk_subbuffer{ d_X, 0, x_sz } }, pc, { (uint32_t)(x_ne), 1, 1});
         ggml_vk_sync_buffers(ctx, subctx);
     }
-    if (y_non_contig) {
+    if (y_needs_reformat) {
         if (ctx->prealloc_y_last_pipeline_used != to_fp16_vk_1.get() ||
             ctx->prealloc_y_last_tensor_used != src1 ||
             ctx->prealloc_y_last_k_padded) {
@@ -6535,7 +6542,7 @@ static void ggml_vk_mul_mat_q_f16(ggml_backend_vk_context * ctx, vk_context& sub
     if (x_non_contig || qx_needs_dequant) {
         ctx->prealloc_x_need_sync = true;
     }
-    if (y_non_contig || quantize_y) {
+    if (y_needs_reformat || quantize_y) {
         ctx->prealloc_y_need_sync = true;
     }
 }
@@ -6660,9 +6667,13 @@ static void ggml_vk_mul_mat_vec_q_f16(ggml_backend_vk_context * ctx, vk_context&
     bool batch_n = ne11 > 1;
 
     const bool x_non_contig = !ggml_vk_dim01_contiguous(src0);
-    const bool y_non_contig = !ggml_vk_dim01_contiguous(src1);
 
-    const bool f16_f32_kernel = src1->type == GGML_TYPE_F32;
+    // BF16 src1 has no mul_mat_vec B-type; widen to F32
+    const bool widen_bf16 = src1->type == GGML_TYPE_BF16;
+    const bool y_non_contig = !ggml_vk_dim01_contiguous(src1) || widen_bf16;
+
+    const ggml_type y_kernel_type = widen_bf16 ? GGML_TYPE_F32 : src1->type;
+    const bool f16_f32_kernel = y_kernel_type == GGML_TYPE_F32;
     bool quantize_y = ctx->device->integer_dot_product && src1->type == GGML_TYPE_F32 && ggml_is_contiguous(src1) && !y_non_contig && (ne11 * ne10) % 4 == 0 && ggml_vk_should_use_mmvq(ctx->device, ne01, ne11, ne10, src0->type);
 
     vk_pipeline to_fp16_vk_0 = nullptr;
@@ -6671,7 +6682,7 @@ static void ggml_vk_mul_mat_vec_q_f16(ggml_backend_vk_context * ctx, vk_context&
         to_fp16_vk_0 = ggml_vk_get_cpy_pipeline(ctx, src0, nullptr, src0->type);
     }
     if (y_non_contig) {
-        to_fp16_vk_1 = ggml_vk_get_cpy_pipeline(ctx, src1, nullptr, src1->type);
+        to_fp16_vk_1 = ggml_vk_get_cpy_pipeline(ctx, src1, nullptr, y_kernel_type);
     } else {
         to_fp16_vk_1 = ggml_vk_get_to_fp16(ctx, src1->type);
     }
@@ -6682,7 +6693,7 @@ static void ggml_vk_mul_mat_vec_q_f16(ggml_backend_vk_context * ctx, vk_context&
 
     if (dmmv == nullptr) {
         // Fall back to f16 dequant mul mat
-        dmmv = ggml_vk_get_dequantize_mul_mat_vec(ctx, src0->type, src1->type, ne11, ne20, ne00);
+        dmmv = ggml_vk_get_dequantize_mul_mat_vec(ctx, src0->type, y_kernel_type, ne11, ne20, ne00);
         quantize_y = false;
     }
 
@@ -6765,7 +6776,7 @@ static void ggml_vk_mul_mat_vec_q_f16(ggml_backend_vk_context * ctx, vk_context&
         ggml_vk_cpy_to_contiguous(ctx, subctx, to_fp16_vk_0, src0, d_Qx, d_X);
     }
     if (y_non_contig) {
-        GGML_ASSERT(y_sz == ggml_type_size(src1->type) * y_ne);
+        GGML_ASSERT(y_sz == ggml_type_size(y_kernel_type) * y_ne);
         if (ctx->prealloc_y_last_pipeline_used != to_fp16_vk_1.get() ||
             ctx->prealloc_y_last_tensor_used != src1 ||
             ctx->prealloc_y_last_k_padded) {
@@ -7251,7 +7262,7 @@ void ggml_vk_mul_mat(ggml_backend_vk_context * ctx, vk_context& subctx, const st
         }
     } else if (ggml_vk_can_use_fwht(ctx, src1, dst)) {
         ggml_vk_fwht(ctx, subctx, src1, dst);
-    } else if (src0->type == GGML_TYPE_F16 && ggml_is_permuted(src0) && ggml_is_permuted(src1) && dst->ne[1] == 1 &&
+    } else if (src0->type == GGML_TYPE_F16 && src1->type == GGML_TYPE_F32 && ggml_is_permuted(src0) && ggml_is_permuted(src1) && dst->ne[1] == 1 &&
         // detect 0213 permutation, and batch size of 1
         src0->nb[0] <= src0->nb[2] &&
         src0->nb[2] <= src0->nb[1] &&
@@ -7264,7 +7275,7 @@ void ggml_vk_mul_mat(ggml_backend_vk_context * ctx, vk_context& subctx, const st
         src0->ne[1] <= ctx->device->properties.limits.maxComputeWorkGroupCount[1] &&
         src1->ne[2] <= ctx->device->properties.limits.maxComputeWorkGroupCount[2]) {
         ggml_vk_mul_mat_vec_p021_f16_f32(ctx, subctx, cgraph, node_idx);
-    } else if (src0->type == GGML_TYPE_F16 && !ggml_is_contiguous(src0) && !ggml_is_transposed(src1) && dst->ne[1] == 1 &&
+    } else if (src0->type == GGML_TYPE_F16 && src1->type == GGML_TYPE_F32 && !ggml_is_contiguous(src0) && !ggml_is_transposed(src1) && dst->ne[1] == 1 &&
                !ggml_is_permuted(src0) && !ggml_is_permuted(src1) &&
                src0->ne[3] <= ctx->device->properties.limits.maxComputeWorkGroupCount[0] &&
                src0->ne[1] <= ctx->device->properties.limits.maxComputeWorkGroupCount[1] &&
@@ -7376,46 +7387,38 @@ static void ggml_vk_mul_mat_id_q_f16(ggml_backend_vk_context * ctx, vk_context&
 #else
     const bool y_decode_vector_staging = false;
 #endif
-    const bool y_non_contig = y_decode_vector_staging ||
-                              (ctx->device->coopmat2 && src1->type == GGML_TYPE_F32) ||
-                              // Intel coopmat1: force f32->f16 conversion so the f16 B-type quant pipeline is used.
-                              (ctx->device->coopmat_support && !ctx->device->coopmat2 &&
-                               ctx->device->vendor_id == VK_VENDOR_ID_INTEL &&
-                               ggml_is_quantized(src0->type) && src1->type == GGML_TYPE_F32) ||
-                              (src0->type == GGML_TYPE_BF16 && src1->type != GGML_TYPE_BF16) ||
-                              !ggml_vk_dim01_contiguous(src1);
+    const bool can_quantize_y = ctx->device->integer_dot_product && src1->type == GGML_TYPE_F32 &&
+                                ggml_is_contiguous(src1) && (ne11 * ne10) % 4 == 0;
+    // Intel coopmat1 matrix cores prefer f16 activations for quantized weights
+    const bool prefer_f16_b = ctx->device->coopmat_support && !ctx->device->coopmat2 &&
+                              ctx->device->vendor_id == VK_VENDOR_ID_INTEL &&
+                              ggml_is_quantized(src0->type) && src1->type == GGML_TYPE_F32;
 
-    const bool y_f32_kernel = src1->type == GGML_TYPE_F32 && !y_non_contig;
+    const ggml_type y_kernel_type = ggml_vk_mul_mat_b_type(ctx, src0->type, src1, f16_type,
+                                        (ggml_prec)dst->op_params[0], true, can_quantize_y, prefer_f16_b);
 
-    bool quantize_y = ctx->device->integer_dot_product && src1->type == GGML_TYPE_F32 && ggml_is_contiguous(src1) && !y_non_contig && (ne11 * ne10) % 4 == 0;
+    const bool quantize_y   = y_kernel_type == GGML_TYPE_Q8_1;
+    const bool y_f32_kernel = y_kernel_type == GGML_TYPE_F32;
 
-    // Check for mmq first
-    const std::vector<vk_matmul_pipeline_pair>* mmp_map = quantize_y ? ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0->type, GGML_TYPE_Q8_1, (ggml_prec)dst->op_params[0], true) : nullptr;
-
-    if (mmp_map == nullptr) {
-        // Fall back to f16 dequant mul mat
-        mmp_map = ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0->type, y_non_contig ? f16_type : src1->type, (ggml_prec)dst->op_params[0], true);
-        quantize_y = false;
-    }
+    const std::vector<vk_matmul_pipeline_pair>* mmp_map =
+        ggml_vk_get_mul_mat_mat_pipeline_map(ctx, src0->type, y_kernel_type, (ggml_prec)dst->op_params[0], true);
 
     const bool qx_needs_dequant = mmp_map == nullptr || x_non_contig;
-    bool qy_needs_dequant = !quantize_y && ((src1->type != f16_type && !y_f32_kernel) || y_non_contig);
 
     if (qx_needs_dequant) {
-        // Fall back to dequant + f16 mulmat
-        mmp_map = ggml_vk_get_mul_mat_mat_pipeline_map(ctx, f16_type, y_f32_kernel ? GGML_TYPE_F32 : f16_type, (ggml_prec)dst->op_params[0], true);
+        // dequant src0 to f16
+        mmp_map = ggml_vk_get_mul_mat_mat_pipeline_map(ctx, f16_type, y_kernel_type, (ggml_prec)dst->op_params[0], true);
     }
 
+    GGML_ASSERT(mmp_map != nullptr);
+
     // Coopmat2 MUL_MAT_ID BK specialization constants in ggml_vk_load_shaders are at most 64.
     const uint32_t y_staged_row_stride = ctx->device->coopmat2 && !quantize_y ? ggml_vk_align_size(ne10, 64) : ne10;
     const bool y_needs_k_padding = ne10 != y_staged_row_stride;
-    const bool y_needs_reformat = y_non_contig || y_needs_k_padding;
-    qy_needs_dequant = qy_needs_dequant || y_needs_k_padding;
-
-    // Not implemented
-    GGML_ASSERT(y_needs_reformat || !qy_needs_dequant);  // NOLINT
 
-    GGML_ASSERT(mmp_map != nullptr);
+    const bool y_needs_reformat = !quantize_y && (!ggml_vk_dim01_contiguous(src1) || y_kernel_type != src1->type ||
+                                                  y_decode_vector_staging || y_needs_k_padding);
+    const bool qy_needs_dequant = y_needs_reformat;
 
     const uint32_t n_per_expert = (uint32_t)CEIL_DIV(nei0 * nei1, n_as);
     const uint32_t kpad = quantize_y ? 0 : ggml_vk_align_size(ne10, ggml_vk_guess_matmul_pipeline_align_map(ctx, *mmp_map, ne01, n_per_expert, true));
@@ -15441,8 +15444,8 @@ static bool ggml_backend_vk_device_supports_op(ggml_backend_dev_t dev, const ggm
                     // So don't support this combination for now.
                     return false;
                 }
-                if (op->src[1]->type == GGML_TYPE_BF16 && op->src[0]->type != GGML_TYPE_BF16) {
-                    // BF16 in src1 is only served by the BF16 x BF16 pipelines
+                if (op->src[1]->type == GGML_TYPE_BF16 && op->src[0]->type != GGML_TYPE_BF16 && op->op != GGML_OP_MUL_MAT) {
+                    // BF16 in src1 (widened to F32/F16) is only wired up for MUL_MAT
                     return false;
                 }
 
diff --git a/ggml/src/ggml-vulkan/vulkan-shaders/vulkan-shaders-gen.cpp b/ggml/src/ggml-vulkan/vulkan-shaders/vulkan-shaders-gen.cpp
index e7e303e50cf..8db456500d5 100644
--- a/ggml/src/ggml-vulkan/vulkan-shaders/vulkan-shaders-gen.cpp
+++ b/ggml/src/ggml-vulkan/vulkan-shaders/vulkan-shaders-gen.cpp
@@ -869,6 +869,7 @@ void process_shaders() {
     string_to_spv("cpy_f16_f32", "copy.comp", {{"A_TYPE", "float16_t"}, {"D_TYPE", "float"}, {"OPTIMIZATION_ERROR_WORKAROUND", "1"}});
     string_to_spv("cpy_f32_bf16","copy.comp", {{"A_TYPE", "float"}, {"D_TYPE", "uint16_t"}, {"DATA_D_BF16", "1"}});
     string_to_spv("cpy_bf16_f32","copy.comp", {{"A_TYPE", "uint16_t"}, {"D_TYPE", "float"}, {"DATA_A_BF16", "1"}});
+    string_to_spv("cpy_bf16_f16","copy.comp", {{"A_TYPE", "uint16_t"}, {"D_TYPE", "float16_t"}, {"DATA_A_BF16", "1"}});
     string_to_spv("contig_cpy_f32_f32", "contig_copy.comp", {{"A_TYPE", "float"}, {"D_TYPE", "float"}});
     string_to_spv("contig_cpy_f32_i32", "contig_copy.comp", {{"A_TYPE", "float"}, {"D_TYPE", "int"}});
     string_to_spv("contig_cpy_i32_f32", "contig_copy.comp", {{"A_TYPE", "int"}, {"D_TYPE", "float"}});
@@ -877,6 +878,7 @@ void process_shaders() {
     string_to_spv("contig_cpy_f16_f32", "contig_copy.comp", {{"A_TYPE", "float16_t"}, {"D_TYPE", "float"}, {"OPTIMIZATION_ERROR_WORKAROUND", "1"}});
     string_to_spv("contig_cpy_f32_bf16","contig_copy.comp",{{"A_TYPE", "float"}, {"D_TYPE", "uint16_t"}, {"DATA_D_BF16", "1"}});
     string_to_spv("contig_cpy_bf16_f32","contig_copy.comp",{{"A_TYPE", "uint16_t"}, {"D_TYPE", "float"}, {"DATA_A_BF16", "1"}});
+    string_to_spv("contig_cpy_bf16_f16","contig_copy.comp",{{"A_TYPE", "uint16_t"}, {"D_TYPE", "float16_t"}, {"DATA_A_BF16", "1"}});
     string_to_spv("cpy_f32_i32", "copy.comp", {{"A_TYPE", "float"}, {"D_TYPE", "int"}});
     string_to_spv("cpy_i32_f32", "copy.comp", {{"A_TYPE", "int"}, {"D_TYPE", "float"}});
 

```

# REVIEW A

# Review of PR #29069: vulkan: support mulmat bf16 activations

The PR is already merged. I read the diff only. I did not build it or run it on hardware.

## Summary
The PR adds BF16 `src1` support to Vulkan `MUL_MAT`, building on #28937. It does three things:
- It adds `cpy_bf16_f16` and `contig_cpy_bf16_f16` pipelines.
- It replaces the tangled `y_non_contig` / `quantize_y` / `qy_needs_dequant` logic with a single helper, `ggml_vk_mul_mat_b_type`.
- It widens BF16 `src1` to F32 in `mul_mat_vec`.

The refactor is a real improvement. `y_kernel_type` is now the single source of truth, and `y_needs_reformat` and `qy_needs_dequant` follow from it. The two `// Not implemented` asserts are gone, and they are now true by construction.

## Positives
- The helper gives a clear priority order: Q8_1, then preferred F16, then native `src1` type, then BF16 to F32, then the F16 fallback.
- `mul_mat_id` now asserts `mmp_map != nullptr` earlier, right after the dequant fallback.
- The p021 and nc `F16` fast paths now require `src1->type == F32`. Without that guard, BF16 `src1` would have reached shaders that assume F32. This is a correct and necessary change.
- `supports_op` rejects BF16 `src1` with a non-BF16 `src0` for anything except `MUL_MAT`. That correctly keeps `MUL_MAT_ID` out of the new path.

## Potential issues and things to verify

1. **Possible coopmat2 behavior change in `ggml_vk_mul_mat_q_f16`.**
   - Before, `coopmat2 && src1 == F32` always forced the F16 conversion.
   - Now `prefer_f16_b` applies only to quantized `src0`. For F16, BF16 or F32 `src0` on coopmat2, an F32 B pipeline is used whenever `available(F32)` is true.
   - That is only equivalent if coopmat2 has no F32 B pipelines for those types. If it does, this is a silent performance or numerics change.
   - Please confirm with a before/after `test-backend-ops perf` run on a coopmat2 device.

2. **Possible coopmat2 behavior change in `ggml_vk_mul_mat_id_q_f16`.**
   - The old `coopmat2 && F32` forced-F16 rule is dropped entirely. Only the Intel coopmat1 rule remains, as `prefer_f16_b`.
   - Coopmat2 also pads K to a multiple of 64 (`y_needs_k_padding`). With `y_kernel_type == F32`, that padding would go through an F32 to F32 copy, which the old code never exercised.
   - `y_decode_vector_staging` has the same change. It used to force an F16 conversion and now keeps `y_kernel_type`.
   - Please verify these combinations on coopmat2 and on any platform that defines `y_decode_vector_staging`.

3. **`prefer_f16_b` ignores `can_quantize_y` in the coopmat1 comment, but the order covers it.**
   - Q8_1 is checked first, so the old "only when MMQ is not taken" condition is preserved. This is fine.
   - A comment saying so, or a note on the precedence, would help future readers.

4. **The `ggml_vk_dim01_contiguous(src1) && available(src1->type)` branch is a little surprising.**
   - For a quantized `src1`, `available(src1->type)` would be false in practice, so it falls through. That is fine.
   - However, `y_needs_reformat` is `!dim01_contiguous || y_kernel_type != src1->type`. A non-contiguous BF16 `src1` with a BF16 `src0` goes to `f16_type == BF16` and is reformatted with a BF16 to BF16 copy. Check that `ggml_vk_get_cpy_pipeline` has a `bf16 -> bf16` entry. The diff only adds `bf16 -> f16`.

5. **`mul_mat_vec` always widens BF16 `src1` to F32, even with a BF16 `src0`.**
   - This costs an extra pass and a buffer. It is acceptable for a first version.
   - The `supports_op` comment says "widened to F32/F16", but the vec path only widens to F32. The comment is slightly imprecise.

6. **Style (minor).**
   - The helper's aligned one-line `if` chain does not match the surrounding code. It is readable, though.
   - The `// perf-heuristic ...` comment is fine. The AGENTS.md rules (ASCII only, concise comments) are followed.

## Test coverage
- The diff touches no tests. The `testing` label suggests `test-backend-ops` coverage came from #28937.
- Please confirm those `MUL_MAT` cases cover the following. They are the combinations whose paths changed here:
  - BF16 `src1` with quantized, F16, F32 and BF16 `src0`.
  - Non-contiguous and permuted BF16 `src1`.
  - `n == 1`, which takes the vec path, and `n > 1`, which takes the matrix path.
  - The p021 and nc shortcuts with BF16 `src1`, which should now fall back to the general path.
- Also confirm that `MUL_MAT_ID` with BF16 `src1` is reported unsupported.
- Run the full suite on at least one device each for coopmat1, coopmat2 and integer-dot, plus a no-coopmat path. The refactor changed the decision logic on all of them.

## Security
No concerns. There is no new external input handling. The only memory-sizing change is the vec-path assert `y_sz == ggml_type_size(y_kernel_type) * y_ne`, which correctly follows the widened type.

## Verdict
This is a sound cleanup with a useful feature. The main residual risk is silent coopmat2 performance or path changes (items 1 and 2). Those are worth a perf comparison, given that the old forced-F16 rules were removed rather than translated.

# REVIEW B

# Review of PR #29069: vulkan: support mulmat bf16 activations

The PR is already merged. It had approvals from CISC and jeffbolznv. I read the diff but did not build it or run any tests. The diff output was truncated in places, so I did not see the whole `ggml_vk_mul_mat_b_type` helper, the `supports_op` change, or any test changes.

## Summary
- It adds `cpy_bf16_f16` and `contig_cpy_bf16_f16` shaders and pipelines, plus the matching branch in `ggml_vk_get_cpy_pipeline`.
- It adds a helper, `ggml_vk_mul_mat_b_type`, that picks the B-type in order: Q8_1, then F16 (or BF16), then the native src1 type, then BF16 widened to F32, then the F16 default.
- `ggml_vk_mul_mat_q_f16` now derives `quantize_y`, `y_f32_kernel` and `y_needs_reformat` from that single `y_kernel_type`. This replaces the tangled `y_non_contig` logic.
- `ggml_vk_mul_mat_vec_q_f16` widens BF16 src1 to F32 first.
- `supports_op` accepts BF16 src1 only for `MUL_MAT`.

## Code quality
The refactor is a clear improvement. A single decision point plus a priority-ordered fallback is much easier to read than the old mix of `y_non_contig`, `quantize_y` and `y_f32_kernel`. The comments are useful. The TODO that asked for this cleanup is removed.

## Potential issues
1. **BF16 to F16 can overflow.** BF16 has the same exponent range as F32, and F16 tops out at 65504. Large activations become `inf` when `cpy_bf16_f16` converts them. This only matters on paths that choose the F16 B-type for BF16 src1, such as the coopmat quant path when `prefer_f16_b` applies or the final `return f16_type` fallback. The fallback to F32 is already in place when an F32 pipeline exists. Check whether the final fallback to `f16_type` can be reached for a BF16 src1 when no F32 pipeline exists. If so, it deserves a comment or a different order. This is probably rare in practice.
2. **The assertion is gone.** `GGML_ASSERT(y_non_contig || !qy_needs_dequant)` was removed. It is now true by construction, because `qy_needs_dequant == y_needs_reformat`, so that's fine. However, nothing now checks that `to_fp16_vk_1` is non-null when `y_needs_reformat` is true. `ggml_vk_get_cpy_pipeline` hits a `GGML_ABORT` when it finds no pipeline, but only if every src and dst type pair is covered. A cheap `GGML_ASSERT(to_fp16_vk_1 != nullptr)` would make failures obvious.
3. **Behaviour change for BF16 src0.** The old code forced a BF16 x BF16 multiply whenever src1 was not BF16. The new order returns `src1->type` (F32) whenever it is contiguous and an F32 pipeline is available. That is probably faster because it skips a conversion. It does change which kernel runs, and therefore the numerics and performance, on existing BF16-weight models. Benchmarks for BF16 models before and after would back this up.
4. **Coopmat1 only partially preserved.** The old rule forced F16 for coopmat1 only when the quantized-src0 MMQ path was not taken. The new code keeps that by checking Q8_1 first. For coopmat2 with F32 src1 and non-quantized src0, the old code always converted to F16 (`y_non_contig`). The new `prefer_f16_b` requires `ggml_is_quantized(src0->type)`, so coopmat2 with F16 or F32 src0 and F32 src1 now uses the F32 B-type kernel if one exists. This may regress performance on coopmat2 devices. Please verify.
5. **`mul_mat_vec` path.** BF16 src1 is always copied to a temporary F32 buffer. This is simple and correct, but it uses extra memory and bandwidth. It is acceptable for a first implementation, because there is no BF16 B-type for the vec shaders.
6. **`MUL_MAT_ID` is unsupported.** BF16 src1 is deliberately limited to `MUL_MAT`. The helper already takes a `mul_mat_id` parameter, so the restriction is clear in the code. A comment saying it is a known limitation would help.

## Performance
- The new copy shaders are trivial and add a small amount of shader-compile and binary size.
- The `prealloc_y_last_pipeline_used` cache still deduplicates the conversion. I did not see anything that would break it.

## Security
No concerns. There is no new external input handling. Buffer sizing for the converted src1 goes through `y_kernel_type`, which should be checked against `qy_sz` and the prealloc size. A BF16 to F32 conversion is twice as large as the source, so the size calculation must use the destination type. I could not confirm this in the truncated portion of the diff.

## Test coverage
- I did not see any `test-backend-ops` additions in the part of the diff I read. The PR depends on #28937, which probably added the BF16 src1 cases to `test-backend-ops`.
- To exercise both the new bf16→f16 path and the mmv widening path, the cases should cover:
  - BF16 src1 with F16, BF16 and quantized src0
  - non-contiguous src1
  - batched cases
  - n=1 (mmv) and larger n (mm)
- Run them with and without coopmat, coopmat2 and integer-dot support. Those flags change the branches taken in the new helper.

## Process
The AI-usage disclosure is marked YES. That meets the template requirement.

## Verdict
This is a sound refactor with a useful feature on top. My follow-up suggestions are:
1. Add a non-null assert for the Y conversion pipeline.
2. Confirm that coopmat2 performance has not regressed.
3. Confirm that BF16 src0 performance has not regressed.
4. Document the F16 overflow risk, or avoid the BF16 to F16 conversion where an F32 pipeline exists.
