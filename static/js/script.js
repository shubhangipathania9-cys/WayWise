document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".budget-fill[data-width]").forEach((bar) => {
    const width = Number.parseFloat(bar.dataset.width);

    if (Number.isFinite(width)) {
      bar.style.width = `${Math.max(0, Math.min(width, 100))}%`;
    }
  });
  // -----------------------------------------
  // THEME TOGGLE
  // -----------------------------------------
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
  } catch (error) {}

  applyTheme(savedTheme);

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const currentTheme = root.getAttribute("data-theme") || "dark";
      const nextTheme = currentTheme === "dark" ? "light" : "dark";

      applyTheme(nextTheme);

      try {
        localStorage.setItem("waywise-theme", nextTheme);
      } catch (error) {}
    });
  }

  // -----------------------------------------
  // INTERACTIVE TRAVEL JOURNAL
  // -----------------------------------------
  const dataElement = document.getElementById("itinerary-data");
  const tripData = document.getElementById("trip-data");
  const leftPage = document.getElementById("left-page");
  const rightPage = document.getElementById("right-page");
  const nextButton = document.querySelector(".right-arrow");
  const previousButton = document.querySelector(".left-arrow");
  const spreadIndicator = document.getElementById("spread-indicator");
  const resetButton = document.getElementById("reset-itinerary");

  // Homepage and other pages do not contain the notebook.
  if (!dataElement || !tripData || !leftPage || !rightPage) return;

  let itinerary;

  try {
    itinerary = JSON.parse(dataElement.textContent);
  } catch (error) {
    console.error("Could not read the itinerary data.", error);
    return;
  }

  const destination = tripData.dataset.destination || "Your destination";
  const days = Number.parseInt(tripData.dataset.days, 10) || 1;
  const travellers = Number.parseInt(tripData.dataset.travellers, 10) || 1;
  const budget = Number.parseInt(tripData.dataset.budget, 10) || 0;

  const storageKey = `waywise-edits-${destination}-${days}`;

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

  function loadEdits() {
    try {
      const saved = localStorage.getItem(storageKey);

      if (saved) {
        const edits = JSON.parse(saved);

        itinerary.forEach((day, dayIndex) => {
          const savedDay = edits[dayIndex];

          if (!savedDay) return;

          day.activities.forEach((activity, activityIndex) => {
            const replacement = savedDay[activityIndex];

            if (typeof replacement === "string") {
              activity.activity = replacement;
            }
          });
        });
      }
    } catch (error) {
      console.warn("Saved itinerary edits could not be loaded.", error);
    }
  }

  function saveEdits() {
    try {
      const edits = itinerary.map((day) =>
        day.activities.map((activity) => activity.activity),
      );

      localStorage.setItem(storageKey, JSON.stringify(edits));
    } catch (error) {
      console.warn("Your edits could not be saved in this browser.", error);
    }
  }

  function createDayHTML(day) {
    const activitiesHTML = day.activities
      .map(
        (activity, index) => `
      <div class="day-section">
        <h3>${escapeHTML(activity.time)}</h3>
        <p
          class="editable-activity"
          contenteditable="true"
          role="textbox"
          aria-label="Edit ${escapeHTML(activity.time)} activity for day ${day.day}"
          data-day="${day.day - 1}"
          data-activity="${index}"
          spellcheck="true"
        >${escapeHTML(activity.activity)}</p>
      </div>
    `,
      )
      .join("");

    return `
      <span class="journal-day-label">YOUR TRAVEL JOURNAL</span>
      <h2>Day ${day.day}</h2>
      <p class="day-subtitle">${escapeHTML(day.title)}</p>
      ${activitiesHTML}
      <div class="notebook-note">
        <p><strong>WayWise tip:</strong> ${escapeHTML(day.tip)}</p>
      </div>
    `;
  }

  function createOverviewHTML() {
    return `
      <span class="journal-day-label">THE JOURNEY STARTS HERE</span>
      <h2>Your Journey Begins</h2>
      <p>A little planning. A lot of discovering.</p>
      <div class="notebook-note">
        <p><strong>Destination:</strong> ${escapeHTML(destination)}</p>
        <p><strong>Travellers:</strong> ${travellers}</p>
        <p><strong>Duration:</strong> ${days} day${days === 1 ? "" : "s"}</p>
        <p><strong>Total budget:</strong> ₹${budget.toLocaleString("en-IN")}</p>
      </div>
      <p class="day-subtitle">
        Built around your preferences. Ready for you to make it your own.
      </p>
    `;
  }

  loadEdits();

  // First spread is the overview and day one.
  // Following spreads show two consecutive trip days.
  const spreads = [
    {
      left: createOverviewHTML(),
      right: createDayHTML(itinerary[0]),
    },
  ];

  for (let index = 1; index < itinerary.length; index += 2) {
    spreads.push({
      left: createDayHTML(itinerary[index]),
      right: itinerary[index + 1]
        ? createDayHTML(itinerary[index + 1])
        : `
          <span class="journal-day-label">UNTIL NEXT TIME</span>
          <h2>Journey Complete</h2>
          <p>Leave room for the unexpected.</p>
          <div class="notebook-note">
            <p>Keep your favourite memories, support local businesses, and travel thoughtfully.</p>
          </div>
        `,
    });
  }

  let currentSpread = 0;

  function showSpread() {
    leftPage.innerHTML = spreads[currentSpread].left;
    rightPage.innerHTML = spreads[currentSpread].right;

    if (previousButton) {
      previousButton.disabled = currentSpread === 0;
    }

    if (nextButton) {
      nextButton.disabled = currentSpread === spreads.length - 1;
    }

    if (spreadIndicator) {
      spreadIndicator.textContent =
        currentSpread === 0
          ? "Trip overview · Day 1"
          : `Journal spread ${currentSpread + 1} of ${spreads.length}`;
    }
  }

  if (nextButton) {
    nextButton.addEventListener("click", () => {
      if (currentSpread < spreads.length - 1) {
        currentSpread += 1;
        showSpread();
      }
    });
  }

  if (previousButton) {
    previousButton.addEventListener("click", () => {
      if (currentSpread > 0) {
        currentSpread -= 1;
        showSpread();
      }
    });
  }

  // Save edited activity text into the current itinerary.
  document.querySelector(".notebook").addEventListener("input", (event) => {
    const target = event.target.closest(".editable-activity");

    if (!target) return;

    const dayIndex = Number.parseInt(target.dataset.day, 10);
    const activityIndex = Number.parseInt(target.dataset.activity, 10);

    if (
      !itinerary[dayIndex] ||
      !itinerary[dayIndex].activities[activityIndex]
    ) {
      return;
    }

    // Store plain text so pasted HTML cannot become page markup.
    const editedText = target.innerText.trim();

    itinerary[dayIndex].activities[activityIndex].activity = editedText;
    saveEdits();
  });

  if (resetButton) {
    resetButton.addEventListener("click", () => {
      try {
        localStorage.removeItem(storageKey);
      } catch (error) {}

      window.location.reload();
    });
  }

  showSpread();
});
