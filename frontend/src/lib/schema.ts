import { z } from "zod";

export const windowSchema = z.object({
  id: z.string(),
  title: z.string(),
  app: z.string(),
  time: z.number(),
});

export const sessionSchema = z.object({
  id: z.string(),
  name: z.string(),
  start: z.number(),
  end: z.number(),
  duration: z.number(),
  windows: z.array(windowSchema),
});

export type STATE = "Active" | "Paused" | "Inactive"
