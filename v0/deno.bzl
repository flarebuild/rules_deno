
_common_attrs = {
    "srcs": attr.label_list(
        allow_files = [
            ".ts",
            ".js",
        ],
        mandatory = True,
    ),
    "deps": attr.label_list(
        # aspects = [],
        # providers = [[DenoInfo]],
    ),
    "entrypoint": attr.label(allow_single_file = True),
    "data": attr.label_list(allow_files = True),
    # "_deno": attr.label(
    #     executable = True,
    #     cfg = "host",
    #     allow_single_file = True,
    #     default = Label("//v0:deno"),
    # ),
}


def _deno_bundle_impl(ctx):
    if len(ctx.attr.entrypoint.files.to_list()) != 1:
        fail("Entrypoint should be exactly one file.")
    ep = ctx.file.entrypoint.path
    output = ctx.actions.declare_file(ctx.attr.name + ".bundle.js")
    ctx.actions.run_shell(
        inputs = ctx.files.srcs + ctx.files.data,
        outputs = [output],
        progress_message = "Bundling %s with deno" % ctx.attr.name,
        command = "~/.deno/bin/deno bundle %s %s" % (ep, output.path),
    )
    return DefaultInfo(
        files = depset([output]),
    )


deno_bundle = rule(
    implementation = _deno_bundle_impl,
    attrs = _common_attrs
)