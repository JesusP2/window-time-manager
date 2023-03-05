import { z } from "zod";

export const activeWindowSchema = z.object({
  title: z.string(),
  app: z.string(),
  time: z.number(), // seconds
});
