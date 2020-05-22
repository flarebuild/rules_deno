import {
  Application,
  Context,
  isHttpError,
  Router,
  RouterContext,
  Status,
} from "https://deno.land/x/oak/mod.ts";

import {
  green,
  cyan,
  bold,
  yellow,
} from "https://deno.land/std@0.52.0/fmt/colors.ts";

import router from "./gen/router.ts";

const app = new Application();
const listenOn = `0.0.0.0:${Deno.env.get("PORT") || 3000}`;

app.use(router.routes());
app.use(router.allowedMethods());

console.log(
  bold("Listening on ") + yellow(listenOn),
);
await app.listen(listenOn);
console.log(bold("Finished."));
