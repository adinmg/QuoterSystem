import asyncio
import time
import httpx

CHATBOT_URL = "http://localhost/download-pdf"

async def make_async_post(url, data):
    timeout = httpx.Timeout(timeout=120)
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=data, timeout=timeout)
        return response

async def make_bulk_requests(url, data):
    tasks = [make_async_post(url, payload) for payload in data]
    responses = await asyncio.gather(*tasks)
    return responses

quotation = [
"Taylor Corp\n 3 Eco-friendly bag\n 15 personalized USB\n 8 polo shirts\n 200 meters of high-resolution printed canvas\n Sales Agent Sarah Lee.",
"GreenTech\n 4 Personalized apron\n 25 metal keychains\n 10 personalized wristwatches\n 50 meters of adhesive vinyl\n Sales Agent Mike Johnson.",
"Bella Boutique\n 7 Silk scarf\n 12 basic ceramic mugs\n 5 embroidered patches\n 100 color flyers\n Sales Agent Emma Brown.",
"Urban Trends\n 8 Promotional poster\n 30 personalized hats\n 7 hooded sweatshirts\n 500 personalized stickers\n Sales Agent Alex White.",
"Healthy Life\n 9 Stainless steel thermos\n 20 personalized towels\n 10 notebooks and pen sets\n 150 meters of low-resolution printed canvas\n Sales Agent Olivia Green.",
"Tech Innovations\n 2 Wireless earphones\n 18 metal pens\n 12 personalized mouse pads\n 200 meters of adhesive vinyl\n Sales Agent David Clark.",
"Fashion Forward\n 5 Personalized blouse\n 8 formal shirts\n 5 foldable umbrellas\n 300 meters of high-resolution printed canvas\n Sales Agent Lily Adams.",
"Creative Minds\n 4 Wall calendar\n 22 promotional caps\n 10 personalized aprons\n 50 personalized stickers\n Sales Agent Ethan Martinez.",
"Sports Gear\n 8 Backpack with logo\n 15 personalized sweaters\n 10 basic short-sleeve shirts\n 100 color flyers\n Sales Agent Ava Turner.",
"Modern Office\n 4 Executive briefcase\n 25 personalized USBs\n 8 digital thermometers\n 50 meters of low-resolution printed canvas\n Sales Agent Noah Davis."
]

request_bodies = [{"text": q} for q in quotation]

start_time = time.perf_counter()
responses = asyncio.run(make_bulk_requests(CHATBOT_URL, request_bodies))
end_time = time.perf_counter()

print(f"Run time: {end_time - start_time} seconds")