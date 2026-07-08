const { test } = require("@playwright/test");
const { argosScreenshot } = require("@argos-ci/playwright");

// The Week 11 dataset is frozen for the run of the cohort, so a given branch's
// dashboard should render byte-identical numbers every time. A pixel diff here
// means the branch (or the shared data) actually changed, not noise.
test("NYC Taxi Metrics app renders", async ({ page }) => {
  await page.goto("/");

  // Streamlit shows a running-man status icon in the top-right while a script
  // executes; wait for it to disappear before snapshotting, or the diff picks
  // up an animation frame instead of the settled page.
  await page
    .getByTestId("stStatusWidget")
    .waitFor({ state: "hidden", timeout: 15_000 })
    .catch(() => {});

  // Wait for either real content (a metric tile) or the expected
  // NotImplementedError TODO warning on starter branches — both are valid,
  // deterministic end states for this frozen dataset.
  await page
    .locator('[data-testid="stMetricValue"], [data-testid="stAlert"]')
    .first()
    .waitFor({ state: "visible", timeout: 15_000 });

  await argosScreenshot(page, "nyc-taxi-metrics-app", { fullPage: true });
});
