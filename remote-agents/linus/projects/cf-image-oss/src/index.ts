export interface Env {
  AI: Ai;
  IMAGES: R2Bucket;
}

function b64ToBytes(base64: string): Uint8Array {
  const bin = atob(base64);
  return Uint8Array.from(bin, (c) => c.codePointAt(0) ?? 0);
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/gen") {
      const prompt = url.searchParams.get("prompt") || "a beautiful woman drinking wine in a cozy bar, cinematic, photorealistic";
      const seed = Math.floor(Math.random() * 1_000_000_000);

      const result = await env.AI.run("@cf/black-forest-labs/flux-1-schnell", {
        prompt,
        steps: 6,
        seed,
      }) as { image: string };

      const key = `generated/${Date.now()}-${seed}.jpg`;
      await env.IMAGES.put(key, b64ToBytes(result.image), {
        httpMetadata: { contentType: "image/jpeg" },
      });

      const publicUrl = `${url.origin}/img/${key}`;
      return Response.json({ key, url: publicUrl, prompt, seed });
    }

    if (url.pathname.startsWith("/img/")) {
      const key = url.pathname.replace(/^\/img\//, "");
      const obj = await env.IMAGES.get(key);
      if (!obj) return new Response("Not found", { status: 404 });
      return new Response(obj.body, {
        headers: {
          "Content-Type": obj.httpMetadata?.contentType || "application/octet-stream",
          "Cache-Control": "public, max-age=31536000, immutable",
        },
      });
    }

    return new Response("ok", { status: 200 });
  },
};
