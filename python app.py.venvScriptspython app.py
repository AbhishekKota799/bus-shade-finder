warning: in the working copy of 'static/css/styles.css', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'static/js/main.js', LF will be replaced by CRLF the next time Git touches it
[1mdiff --git a/static/css/styles.css b/static/css/styles.css[m
[1mindex d681a20..c8448c8 100644[m
[1m--- a/static/css/styles.css[m
[1m+++ b/static/css/styles.css[m
[36m@@ -178,6 +178,13 @@[m [mbutton:disabled {[m
     opacity: 0.72;[m
 }[m
 [m
[32m+[m[32m.primary-action {[m
[32m+[m[32m    width: 100%;[m
[32m+[m[32m    min-height: 56px;[m
[32m+[m[32m    margin-top: 4px;[m
[32m+[m[32m    font-size: 1.05rem;[m
[32m+[m[32m}[m
[32m+[m
 .loading-overlay {[m
     position: fixed;[m
     inset: 0;[m
[36m@@ -239,6 +246,10 @@[m [mbutton:disabled {[m
     margin: 0;[m
 }[m
 [m
[32m+[m[32m.recommendation-details {[m
[32m+[m[32m    margin-bottom: 20px;[m
[32m+[m[32m}[m
[32m+[m
 .result-list div {[m
     display: flex;[m
     justify-content: space-between;[m
[36m@@ -281,38 +292,6 @@[m [mdd {[m
     margin: 0;[m
 }[m
 [m
[31m-@media (max-width: 760px) {[m
[31m-    .nav {[m
[31m-        align-items: flex-start;[m
[31m-        flex-direction: column;[m
[31m-        justify-content: center;[m
[31m-        padding: 16px 0;[m
[31m-    }[m
[31m-[m
[31m-    .hero {[m
[31m-        padding-top: 36px;[m
[31m-    }[m
[31m-[m
[31m-    .planner,[m
[31m-    .form-row {[m
[31m-        grid-template-columns: 1fr;[m
[31m-    }[m
[31m-[m
[31m-    .panel {[m
[31m-        padding: 22px;[m
[31m-    }[m
[31m-[m
[31m-    .result-list div {[m
[31m-        align-items: flex-start;[m
[31m-        flex-direction: column;[m
[31m-        gap: 4px;[m
[31m-    }[m
[31m-[m
[31m-    dd {[m
[31m-        text-align: left;[m
[31m-    }[m
[31m-}[m
[31m-[m
 .error-card {[m
     display: grid;[m
     grid-template-columns: auto 1fr;[m
[36m@@ -618,8 +597,8 @@[m [mdd {[m
     box-shadow: var(--shadow-soft);[m
 }[m
 [m
[31m-.timeline-item span,[m
[31m-.timeline-item small,[m
[32m+[m[32m.timeline-item time,[m
[32m+[m[32m.timeline-exposures,[m
 .timeline-empty {[m
     color: var(--muted);[m
 }[m
[36m@@ -628,14 +607,12 @@[m [mdd {[m
     color: var(--primary-dark);[m
 }[m
 [m
[31m-.timeline-item small {[m
[32m+[m[32m.timeline-exposures {[m
     grid-column: 1 / -1;[m
[31m-}[m
[31m-[m
[31m-@media (max-width: 760px) {[m
[31m-    .timeline-item {[m
[31m-        grid-template-columns: 1fr;[m
[31m-    }[m
[32m+[m[32m    display: flex;[m
[32m+[m[32m    flex-wrap: wrap;[m
[32m+[m[32m    gap: 4px 16px;[m
[32m+[m[32m    font-size: 0.9rem;[m
 }[m
 [m
 @media (max-width: 760px) {[m
[36m@@ -648,6 +625,9 @@[m [mdd {[m
     }[m
 [m
     .nav {[m
[32m+[m[32m        align-items: flex-start;[m
[32m+[m[32m        flex-direction: column;[m
[32m+[m[32m        justify-content: center;[m
         gap: 14px;[m
         padding: 18px 0;[m
     }[m
[36m@@ -669,9 +649,14 @@[m [mdd {[m
         margin-bottom: 16px;[m
     }[m
 [m
[31m-    .planner,[m
[32m+[m[32m    .planner {[m
[32m+[m[32m        grid-template-columns: 1fr;[m
[32m+[m[32m        gap: 16px;[m
[32m+[m[32m    }[m
[32m+[m
     .form-row {[m
[31m-        gap: 18px;[m
[32m+[m[32m        grid-template-columns: 1fr;[m
[32m+[m[32m        gap: 14px;[m
     }[m
 [m
     .panel {[m
[36m@@ -684,6 +669,24 @@[m [mdd {[m
         font-size: 1rem;[m
     }[m
 [m
[32m+[m[32m    .trip-form {[m
[32m+[m[32m        gap: 16px;[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    .trip-form label {[m
[32m+[m[32m        margin-bottom: 8px;[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    .result-list div {[m
[32m+[m[32m        align-items: flex-start;[m
[32m+[m[32m        flex-direction: column;[m
[32m+[m[32m        gap: 4px;[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    dd {[m
[32m+[m[32m        text-align: left;[m
[32m+[m[32m    }[m
[32m+[m
     .route-map {[m
         height: 340px;[m
     }[m
[36m@@ -720,14 +723,14 @@[m [mdd {[m
     }[m
 [m
     .bus-shell {[m
[31m-        min-height: 260px;[m
[32m+[m[32m        min-height: clamp(250px, 76vw, 290px);[m
         grid-template-columns: minmax(0, 1fr) 20px minmax(0, 1fr);[m
         gap: 8px;[m
         padding: 22px 14px;[m
     }[m
 [m
     .seat-column span {[m
[31m-        min-height: 42px;[m
[32m+[m[32m        min-height: 44px;[m
     }[m
 [m
     .direction-arrow {[m
[36m@@ -736,15 +739,19 @@[m [mdd {[m
 [m
     .timeline-list {[m
         max-height: none;[m
[31m-        overflow: visible;[m
[32m+[m[32m        overflow-x: auto;[m
[32m+[m[32m        overflow-y: visible;[m
[32m+[m[32m        overscroll-behavior-inline: contain;[m
[32m+[m[32m        scrollbar-width: thin;[m
     }[m
 [m
     .timeline-item {[m
[32m+[m[32m        grid-template-columns: 1fr;[m
         gap: 6px;[m
         padding: 14px;[m
     }[m
 [m
[31m-    .timeline-item span {[m
[32m+[m[32m    .timeline-item time {[m
         font-size: 0.92rem;[m
     }[m
 [m
[36m@@ -752,8 +759,11 @@[m [mdd {[m
         font-size: 1.1rem;[m
     }[m
 [m
[31m-    .timeline-item small {[m
[32m+[m[32m    .timeline-exposures {[m
[32m+[m[32m        display: grid;[m
[32m+[m[32m        gap: 4px;[m
         line-height: 1.6;[m
[32m+[m[32m        overflow-wrap: anywhere;[m
     }[m
 }[m
 [m
[36m@@ -763,7 +773,7 @@[m [mdd {[m
     }[m
 [m
     .panel {[m
[31m-        padding: 18px 12px;[m
[32m+[m[32m        padding: 18px 14px;[m
     }[m
 [m
     .bus-visual {[m
[1mdiff --git a/static/js/main.js b/static/js/main.js[m
[1mindex 66f5423..eabbce3 100644[m
[1m--- a/static/js/main.js[m
[1m+++ b/static/js/main.js[m
[36m@@ -9,6 +9,18 @@[m [mconst loadingMessages = [[m
 [m
 let loadingTimer = null;[m
 [m
[32m+[m[32mfunction stopLoadingMessages() {[m
[32m+[m[32m    if (loadingTimer) {[m
[32m+[m[32m        window.clearInterval(loadingTimer);[m
[32m+[m[32m        loadingTimer = null;[m
[32m+[m[32m    }[m
[32m+[m
[32m+[m[32m    if (loadingOverlay) {[m
[32m+[m[32m        loadingOverlay.classList.remove('is-visible');[m
[32m+[m[32m        loadingOverlay.setAttribute('aria-hidden', 'true');[m
[32m+[m[32m    }[m
[32m+[m[32m}[m
[32m+[m
 function startLoadingMessages() {[m
     if (!loadingOverlay || !loadingStatus) {[m
         return;[m
[36m@@ -38,6 +50,7 @@[m [mif (tripForm) {[m
         const submitButton = tripForm.querySelector('button[type="submit"]');[m
         if (submitButton) {[m
             submitButton.disabled = true;[m
[32m+[m[32m            submitButton.setAttribute('aria-busy', 'true');[m
             submitButton.textContent = 'Analyzing...';[m
         }[m
 [m
[36m@@ -45,3 +58,5 @@[m [mif (tripForm) {[m
     });[m
 }[m
 [m
[32m+[m[32mwindow.addEventListener('pageshow', stopLoadingMessages);[m
[32m+[m
[1mdiff --git a/templates/index.html b/templates/index.html[m
[1mindex bde8ae8..eca43e9 100644[m
[1m--- a/templates/index.html[m
[1m+++ b/templates/index.html[m
[36m@@ -39,7 +39,7 @@[m
             <div class="panel">[m
                 <h2 id="planner-title">Plan your journey</h2>[m
                 {% if errors %}[m
[31m-                    <div class="error-card" role="alert" aria-labelledby="form-error-title">[m
[32m+[m[32m                    <div id="form-errors" class="error-card" role="alert" aria-labelledby="form-error-title">[m
                         <span class="error-icon" aria-hidden="true">!</span>[m
                         <p id="form-error-title">Please review your journey details:</p>[m
                         <ul>[m
[36m@@ -51,23 +51,23 @@[m
                 {% endif %}[m
                 <form id="trip-form" class="trip-form" method="post" action="{{ url_for('home') }}#results">[m
                     <label for="start_location">Starting Location</label>[m
[31m-                    <input id="start_location" name="start_location" type="text" placeholder="Enter starting point" value="{{ start_location | default('') }}" required>[m
[32m+[m[32m                    <input id="start_location" name="start_location" type="text" placeholder="Enter starting point" value="{{ start_location | default('') }}"{% if errors %} aria-describedby="form-errors" aria-invalid="true"{% endif %} required>[m
 [m
                     <label for="destination">Destination</label>[m
[31m-                    <input id="destination" name="destination" type="text" placeholder="Enter destination" value="{{ destination | default('') }}" required>[m
[32m+[m[32m                    <input id="destination" name="destination" type="text" placeholder="Enter destination" value="{{ destination | default('') }}"{% if errors %} aria-describedby="form-errors" aria-invalid="true"{% endif %} required>[m
 [m
                     <div class="form-row">[m
                         <div>[m
                             <label for="departure_date">Departure Date</label>[m
[31m-                            <input id="departure_date" name="departure_date" type="date" value="{{ departure_date | default('') }}" required>[m
[32m+[m[32m                            <input id="departure_date" name="departure_date" type="date" value="{{ departure_date | default('') }}"{% if errors %} aria-describedby="form-errors" aria-invalid="true"{% endif %} required>[m
                         </div>[m
                         <div>[m
                             <label for="departure_time">Departure Time</label>[m
[31m-                            <input id="departure_time" name="departure_time" type="time" value="{{ departure_time | default('') }}" required>[m
[32m+[m[32m                            <input id="departure_time" name="departure_time" type="time" value="{{ departure_time | default('') }}"{% if errors %} aria-describedby="form-errors" aria-invalid="true"{% endif %} required>[m
                         </div>[m
                     </div>[m
 [m
[31m-                    <button type="submit">Find Best Seat</button>[m
[32m+[m[32m                    <button class="primary-action" type="submit">Find My Shade</button>[m
                 </form>[m
             </div>[m
 [m
[36m@@ -102,13 +102,7 @@[m
                             </div>[m
                             <p>{{ recommendation_reason | default('Submit a journey to see the recommendation details.') }}</p>[m
                         </div>[m
[31m-                        <div id="route-map" class="route-map" data-route='{{ route_coordinates | default([]) | tojson }}' data-start='{{ start_marker | default(none) | tojson }}' data-destination='{{ destination_marker | default(none) | tojson }}' data-timeline='{{ journey_timeline | default([]) | tojson }}' aria-label="Retrieved bus route map"></div>[m
[31m-                        <p id="map-empty-message" class="map-empty-message">No route is available yet. Submit a journey to show it on the map.</p>[m
[31m-                        <div class="map-summary" aria-label="Route map summary">[m
[31m-                            <span>Distance: <strong>{{ route_distance | default('--') }}</strong></span>[m
[31m-                            <span>Duration: <strong>{{ estimated_travel_time | default('--') }}</strong></span>[m
[31m-                        </div>[m
[31m-                        <dl class="result-list">[m
[32m+[m[32m                        <dl class="result-list recommendation-details" aria-label="Recommendation details">[m
                             <div>[m
                                 <dt>Confidence</dt>[m
                                 <dd>{{ shade_score | default('--') }}{% if shade_score is defined and shade_score != '--' %}%{% endif %}</dd>[m
[36m@@ -130,15 +124,24 @@[m
                                 <dd>{{ turn_count | default('--') }}</dd>[m
                             </div>[m
                         </dl>[m
[32m+[m[32m                        <div id="route-map" class="route-map" data-route='{{ route_coordinates | default([]) | tojson }}' data-start='{{ start_marker | default(none) | tojson }}' data-destination='{{ destination_marker | default(none) | tojson }}' data-timeline='{{ journey_timeline | default([]) | tojson }}' role="region" tabindex="0" aria-label="Retrieved bus route map"></div>[m
[32m+[m[32m                        <p id="map-empty-message" class="map-empty-message">No route is available yet. Submit a journey to show it on the map.</p>[m
[32m+[m[32m                        <div class="map-summary" aria-label="Route map summary">[m
[32m+[m[32m                            <span>Distance: <strong>{{ route_distance | default('--') }}</strong></span>[m
[32m+[m[32m                            <span>Duration: <strong>{{ estimated_travel_time | default('--') }}</strong></span>[m
[32m+[m[32m                        </div>[m
 [m
                         <section class="timeline" aria-labelledby="timeline-title">[m
                             <h3 id="timeline-title">Journey timeline</h3>[m
                             <div class="timeline-list">[m
                                 {% for item in journey_timeline %}[m
                                     <article class="timeline-item">[m
[31m-                                        <span>{{ item.time }}</span>[m
[32m+[m[32m                                        <time datetime="{{ item.time }}">{{ item.time }}</time>[m
                                         <strong>{{ item.recommended_side }}</strong>[m
[31m-                                        <small>Left: {{ item.left_exposure }} | Right: {{ item.right_exposure }}</small>[m
[32m+[m[32m                                        <div class="timeline-exposures">[m
[32m+[m[32m                                            <span>Left sunlight: {{ item.left_exposure }}</span>[m
[32m+[m[32m                                            <span>Right sunlight: {{ item.right_exposure }}</span>[m
[32m+[m[32m                                        </div>[m
                                     </article>[m
                                 {% endfor %}[m
                             </div>[m
