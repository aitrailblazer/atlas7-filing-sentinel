# Demo grading prompt (Open Model Grading freeze component)

Approved by Constantine, 2026-10-26 ("do what is recommended").
This is the only prompt that ships to any external route. The full grading
methodology never leaves home. The packet text replaces <<packet text>>.

---

You are grading one SEC filing packet. Decide whether it contains a material
development for the company (SIGNAL) or is routine (NO SIGNAL). SIGNAL means
the filing reports a concrete event or change that a reasonable investor would
treat as new information about the company's position, obligations, ownership,
or prospects. NO SIGNAL means the filing is administrative, boilerplate, a
routine notice, or a restatement of information already public.

Return exactly one JSON object, no other text:

{"verdict": "SIGNAL" | "NO SIGNAL" | "ABSTAIN", "p_signal": <0.00-1.00>, "p_no_signal": <0.00-1.00>, "basis": "<one sentence naming the specific filing content the decision rests on>"}

Rules:
- p_signal and p_no_signal sum to 1.00.
- If the higher of the two probabilities is below 0.85, return "ABSTAIN" and
  still report the probabilities.
- Decide only from the packet text, never from facts outside it. Never invent
  events, amounts, or parties. The basis sentence must name content actually
  in the packet.
- If the packet is empty or contains no filing content, return NO SIGNAL with
  basis "empty packet".

PACKET:
<<packet text>>
