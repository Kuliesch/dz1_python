"""Тест відкритої дифузійної моделі (SD-Turbo) на CPU."""

import argparse
import time
from pathlib import Path

import torch
from diffusers import AutoPipelineForText2Image


def main() -> None:
    parser = argparse.ArgumentParser(description="Тест генерації зображення дифузійною моделлю")
    parser.add_argument(
        "--model",
        default="stabilityai/sd-turbo",
        help="Hugging Face ID моделі (за замовчуванням: stabilityai/sd-turbo)",
    )
    parser.add_argument(
        "--prompt",
        default="A cozy Ukrainian village at sunset, warm light, photorealistic",
        help="Текстовий промпт",
    )
    parser.add_argument("--steps", type=int, default=4, help="Кількість кроків інференсу")
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", default="output/test_image.png")
    args = parser.parse_args()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    print(f"Пристрій: {device}")
    print(f"Модель: {args.model}")
    print(f"Промпт: {args.prompt}")

    print("Завантаження моделі...")
    load_start = time.perf_counter()
    pipe = AutoPipelineForText2Image.from_pretrained(
        args.model,
        torch_dtype=dtype,
        variant="fp16" if device == "cuda" else None,
    )
    pipe = pipe.to(device)
    if device == "cpu":
        pipe.enable_attention_slicing()
    print(f"Модель завантажено за {time.perf_counter() - load_start:.1f} с")

    generator = torch.Generator(device=device).manual_seed(args.seed)

    print(f"Генерація ({args.steps} кроків, {args.width}x{args.height})...")
    gen_start = time.perf_counter()
    result = pipe(
        prompt=args.prompt,
        num_inference_steps=args.steps,
        guidance_scale=0.0,
        width=args.width,
        height=args.height,
        generator=generator,
    )
    elapsed = time.perf_counter() - gen_start
    print(f"Генерація завершена за {elapsed:.1f} с")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.images[0].save(output_path)
    print(f"Збережено: {output_path.resolve()}")


if __name__ == "__main__":
    main()
