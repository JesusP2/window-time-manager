import { describe, it } from "vitest";
import { getTimeUnits } from "./time-formatter";

const date = {
  seconds: 0,
  minutes: 0,
  hours: 0,
  days: 0,
  weeks: 0,
};

describe("time formatter", () => {
  it.concurrent("test #1", ({ expect }) => {
    expect(getTimeUnits(10)).toEqual({ ...date, seconds: 10 });
  });
  it.concurrent("test #2", ({ expect }) => {
    expect(getTimeUnits(110)).toEqual({ ...date, seconds: 50, minutes: 1 });
    expect(getTimeUnits(120)).toEqual({ ...date, minutes: 2 });
    expect(getTimeUnits(130)).toEqual({ ...date, seconds: 10, minutes: 2 });
  });
  it.concurrent("test #3", ({ expect }) => {
    expect(getTimeUnits(3600)).toEqual({ ...date, hours: 1 });
  });
  it.concurrent("test #4", ({ expect }) => {
    expect(getTimeUnits(3820)).toEqual({
      ...date,
      hours: 1,
      minutes: 3,
      seconds: 40,
    });
    expect(getTimeUnits(7150)).toEqual({
      ...date,
      hours: 1,
      minutes: 59,
      seconds: 10,
    });
    expect(getTimeUnits(7210)).toEqual({ ...date, hours: 2, seconds: 10 });
  });
  it.concurrent("test #5", ({ expect }) => {
    expect(getTimeUnits(86040)).toEqual({ ...date, hours: 23, minutes: 54 });
    expect(getTimeUnits(86399)).toEqual({
      ...date,
      hours: 23,
      minutes: 59,
      seconds: 59,
    });
  });
  it.concurrent("test #6", ({ expect }) => {
    expect(getTimeUnits(86401)).toEqual({ ...date, days: 1, seconds: 1 });
    expect(getTimeUnits(86399 + 86400)).toEqual({
      ...date,
      days: 1,
      hours: 23,
      minutes: 59,
      seconds: 59,
    });
  });
  it.concurrent("test #7", ({ expect }) => {
    expect(getTimeUnits(604799)).toEqual({
      ...date,
      days: 6,
      hours: 23,
      minutes: 59,
      seconds: 59,
    });
    expect(getTimeUnits(604800)).toEqual({
      ...date,
      weeks: 1,
    });

    expect(getTimeUnits(604799 + 604800)).toEqual({
      ...date,
      weeks: 1,
      days: 6,
      hours: 23,
      minutes: 59,
      seconds: 59,
    });
  });
});
