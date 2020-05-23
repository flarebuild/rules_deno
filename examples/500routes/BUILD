load("//v0:deno.bzl", "deno_bundle")

# deno_bundle(
#     name = "services",
#     srcs = glob(
#         ["gen/services/*.ts"],
#         exclude = ["*.spec.ts"],
#     ),
#     deps = [
#     ],
#     entrypoint = "gen/services/mod.ts",
#     visibility = ["//visibility:public"]
# )

# deno_bundle(
#     name = "controllers",
#     srcs = glob(
#         ["gen/controllers/*.ts"],
#         exclude = ["*.spec.ts"],
#     ),
#     deps = [
#         ":services",
#     ],
#     entrypoint = "gen/controllers/mod.ts",
#     visibility = ["//visibility:public"]
# )

deno_bundle(
    name = "500routes",
    srcs = glob( # eventually should just be index.ts
        ["**/*.ts"],
        exclude = ["*.spec.ts"],
    ),
    deps = [
        # ":controllers",
    ],
    entrypoint = "index.ts",
    visibility = ["//visibility:public"]
)