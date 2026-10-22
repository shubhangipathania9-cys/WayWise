/* ========================================
   WAYWISE - MAIN JAVASCRIPT
   ======================================== */

document.addEventListener("DOMContentLoaded", () => {
  /* ---------- LIGHT / DARK THEME ---------- */

  const themeToggle = document.getElementById("theme-toggle");
  const root = document.documentElement;
  const themeColorMeta = document.querySelector('meta[name="theme-color"]');

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);

    if (themeColorMeta) {
      themeColorMeta.setAttribute(
        "content",
        theme === "dark" ? "#171a20" : "#f7f9fc",
      );
    }

    if (themeToggle) {
      const nextTheme = theme === "dark" ? "light" : "dark";
      themeToggle.setAttribute("aria-label", `Switch to ${nextTheme} mode`);
      themeToggle.setAttribute("title", `Switch to ${nextTheme} mode`);
      themeToggle.setAttribute("aria-pressed", String(theme === "light"));
    }
  }

  let savedTheme = "dark";

  try {
    savedTheme = localStorage.getItem("waywise-theme") || "dark";
  } catch (error) {
    // Continue using the default theme if storage is unavailable.
  }

  applyTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = root.getAttribute("data-theme") || "dark";
      const nextTheme = currentTheme === "dark" ? "light" : "dark";

      applyTheme(nextTheme);

      try {
        localStorage.setItem("waywise-theme", nextTheme);
      } catch (error) {
        // Theme still works for the current page if storage is unavailable.
      }
    });
  }

  /* ---------- ITINERARY NOTEBOOK ---------- */

  const nextButton = document.querySelector(".right-arrow");
  const previousButton = document.querySelector(".left-arrow");
  const leftPage = document.getElementById("left-page");
  const rightPage = document.getElementById("right-page");
  const tripData = document.getElementById("trip-data");

  // Other pages do not contain the notebook, so safely skip this section.
  if (!tripData || !leftPage || !rightPage) {
    return;
  }

  const destination = tripData.dataset.destination || "Your destination";
  const days = Math.max(
    1,
    Math.min(30, Number.parseInt(tripData.dataset.days, 10) || 1),
  );
  const travellers = tripData.dataset.travellers || "1";
  const budget = tripData.dataset.budget || "0";

  // Escape user-provided values before inserting them into HTML.
  function escapeHTML(value) {
    return String(value).replace(/[&<>"']/g, (character) => {
      const entities = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;",
      };

      return entities[character];
    });
  }

  const safeDestination = escapeHTML(destination);
  const safeTravellers = escapeHTML(travellers);
  const safeBudget = escapeHTML(Number(budget).toLocaleString("en-IN"));

  const dailyPlans = [
    {
      subtitle: "Arrival & Local Exploration",
      morning: "Arrive, settle in, and get familiar with the area.",
      afternoon: "Explore a nearby attraction or a local neighbourhood.",
      evening: "Try local food and enjoy a relaxed evening.",
    },
    {
      subtitle: "Discover Something New",
      morning: "Start with a popular local attraction.",
      afternoon: "Explore a cultural spot or a nearby hidden gem.",
      evening: "Enjoy local cuisine and explore at your own pace.",
    },
    {
      subtitle: "Culture & Local Experiences",
      morning: "Discover the area's history, architecture, or nature.",
      afternoon: "Visit a local market or try a regional experience.",
      evening: "Find a scenic spot and unwind.",
    },
    {
      subtitle: "Nature & Adventure",
      morning: "Enjoy an outdoor activity suited to the destination.",
      afternoon: "Explore a nature spot or take a scenic walk.",
      evening: "Rest, recharge, and enjoy a local dinner.",
    },
    {
      subtitle: "Slow Travel Day",
      morning: "Enjoy a leisurely breakfast and explore nearby.",
      afternoon: "Spend time at a place that interests you most.",
      evening: "Discover a quieter corner of the destination.",
    },
  ];

  function getDailyPlan(dayNumber) {
    // Reuse the curated plan patterns for longer trips.
    return dailyPlans[(dayNumber - 1) % dailyPlans.length];
  }

  function createDayHTML(dayNumber) {
    const plan = getDailyPlan(dayNumber);

    return `
      <h2>Day ${dayNumber}</h2>
      <p class="day-subtitle">${plan.subtitle}</p>

      <div class="day-section">
        <h3>Morning</h3>
        <p>${plan.morning}</p>
      </div>

      <div class="day-section">
        <h3>Afternoon</h3>
        <p>${plan.afternoon}</p>
      </div>

      <div class="day-section">
        <h3>Evening</h3>
        <p>${plan.evening}</p>
      </div>

      <div class="notebook-note">
        <p><strong>Traveller tip:</strong> Keep some free time for unexpected discoveries.</p>
      </div>
    `;
  }

  const spreads = [
    {
      left: `
        <h2>Your Journey Begins</h2>
        <p>Your trip overview, built around your travel preferences.</p>

        <div class="notebook-note">
          <p><strong>Destination:</strong> ${safeDestination}</p>
          <p><strong>Travellers:</strong> ${safeTravellers}</p>
          <p><strong>Duration:</strong> ${days} day${days === 1 ? "" : "s"}</p>
          <p><strong>Budget:</strong> ₹${safeBudget}</p>
        </div>

        <p class="day-subtitle">
          Your itinerary is a starting point. Adjust activities to suit your pace.
        </p>
      `,
      right: createDayHTML(1),
    },
  ];

  // Add overlapping day spreads so the notebook can be browsed naturally.
  for (let day = 2; day <= days; day++) {
    spreads.push({
      left: createDayHTML(day - 1),
      right: createDayHTML(day),
    });
  }

  let currentSpread = 0;

  function showSpread() {
    leftPage.innerHTML = spreads[currentSpread].left;
    rightPage.innerHTML = spreads[currentSpread].right;

    if (previousButton) {
      previousButton.disabled = currentSpread === 0;
      previousButton.setAttribute(
        "aria-label",
        "View previous itinerary pages",
      );
    }

    if (nextButton) {
      nextButton.disabled = currentSpread === spreads.length - 1;
      nextButton.setAttribute("aria-label", "View next itinerary pages");
    }
  }

  if (nextButton) {
    nextButton.addEventListener("click", () => {
      if (currentSpread < spreads.length - 1) {
        currentSpread++;
        showSpread();
      }
    });
  }

  if (previousButton) {
    previousButton.addEventListener("click", () => {
      if (currentSpread > 0) {
        currentSpread--;
        showSpread();
      }
    });
  }

  showSpread();
});
