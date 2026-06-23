document.addEventListener('DOMContentLoaded', () => {
    const locSelect = document.getElementById('location');
    const cuisineInput = document.getElementById('cuisine');
    const budgetBtns = document.querySelectorAll('.budget-btn');
    const ratingInput = document.getElementById('rating');
    const ratingVal = document.getElementById('rating-val');
    const addInput = document.getElementById('additional');
    const topKInput = document.getElementById('top_k');
    const submitBtn = document.getElementById('submit-btn');
    const summaryBox = document.getElementById('summary-box');
    const summaryText = document.getElementById('summary-text');
    const resultsGrid = document.getElementById('results-grid');
    
    let selectedBudget = 'medium';

    // Budget Selection Logic
    budgetBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            // Reset all
            budgetBtns.forEach(b => {
                b.className = 'py-2 text-xs font-bold rounded-lg text-on-surface hover:bg-white/5 transition-all budget-btn';
            });
            // Set active
            e.target.className = 'py-2 text-xs font-bold rounded-lg bg-primary-container text-white shadow-lg budget-btn';
            selectedBudget = e.target.getAttribute('data-budget');
        });
    });

    // Fetch Locations
    fetch('/api/locations')
        .then(r => r.json())
        .then(data => {
            locSelect.innerHTML = '';
            data.forEach(loc => {
                const opt = document.createElement('option');
                opt.value = loc;
                opt.textContent = loc.charAt(0).toUpperCase() + loc.slice(1);
                locSelect.appendChild(opt);
            });
        }).catch(err => console.error("Failed to load locations", err));

    // Fetch Cuisines
    fetch('/api/cuisines')
        .then(r => r.json())
        .then(data => {
            cuisineInput.innerHTML = '<option value="">Any Cuisine</option>';
            data.forEach(c => {
                const opt = document.createElement('option');
                opt.value = c;
                opt.textContent = c;
                cuisineInput.appendChild(opt);
            });
        }).catch(err => console.error("Failed to load cuisines", err));

    // Clear initial hardcoded cards
    resultsGrid.innerHTML = '';

    // Handle Submit
    submitBtn.addEventListener('click', async () => {
        // UI Loading State
        const originalText = submitBtn.textContent;
        submitBtn.textContent = "Processing with AI...";
        submitBtn.disabled = true;
        submitBtn.style.opacity = '0.7';
        
        summaryBox.classList.add('hidden');
        resultsGrid.innerHTML = '<div class="text-on-surface-variant italic col-span-full">Analyzing thousands of reviews to find your perfect match...</div>';

        const payload = {
            location: locSelect.value || 'bangalore',
            budget: selectedBudget,
            cuisine: cuisineInput.value || null,
            min_rating: parseFloat(ratingInput.value),
            additional_preferences: addInput.value || null,
            top_k: parseInt(topKInput.value) || 5
        };

        try {
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                resultsGrid.innerHTML = `<div class="text-error col-span-full">Error: ${data.detail || 'Failed to fetch recommendations'}</div>`;
                return;
            }

            renderResults(data);
        } catch (err) {
            console.error(err);
            resultsGrid.innerHTML = `<div class="text-error col-span-full">An error occurred: ${err.message}</div>`;
        } finally {
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
            submitBtn.style.opacity = '1';
        }
    });

    function renderResults(data) {
        resultsGrid.innerHTML = '';
        
        if (data.recommendations && data.recommendations.length > 0) {
            summaryBox.classList.remove('hidden');
            summaryText.innerHTML = data.summary || `Found ${data.recommendations.length} matching restaurants for your criteria.`;
            
            data.recommendations.forEach(rec => {
                const card = document.createElement('div');
                card.className = "glass-panel rounded-[2rem] overflow-hidden glass-card-hover transition-all duration-300 group";
                
                // Generic elegant dining placeholder images based on rank
                const imgUrl = `https://source.unsplash.com/800x600/?restaurant,dining,${rec.cuisine.split(',')[0]}&sig=${rec.rank}`;

                card.innerHTML = `
                    <div class="p-6 relative mt-4">
                        <div class="absolute -top-4 left-4 bg-primary-container text-white px-4 py-1 rounded-full font-headline text-sm font-bold shadow-xl z-10">
                            #${rec.rank} RECOMMENDED
                        </div>
                        <div class="flex justify-between items-start mb-2 mt-2">
                            <h3 class="font-title-md text-title-md font-bold text-white line-clamp-1" title="${rec.restaurant_name}">${rec.restaurant_name}</h3>
                            <div class="flex items-center text-secondary shrink-0 ml-2">
                                <span class="material-symbols-outlined text-sm" data-icon="star" style="font-variation-settings: 'FILL' 1;">star</span>
                                <span class="ml-1 text-sm font-bold">${parseFloat(rec.rating).toFixed(1)}</span>
                            </div>
                        </div>
                        <p class="text-on-surface-variant text-sm mb-4 line-clamp-1">${rec.cuisine}</p>
                        <div class="flex items-center gap-4 mb-6">
                            <div class="flex flex-col">
                                <span class="text-[10px] text-on-surface-variant font-bold">COST FOR TWO</span>
                                <span class="text-primary font-bold">${rec.estimated_cost}</span>
                            </div>
                        </div>
                        <div class="bg-white/5 p-4 rounded-xl border border-white/5 mb-6 min-h-[100px]">
                            <p class="text-sm italic text-on-surface-variant line-clamp-4">
                                "${rec.explanation}"
                            </p>
                        </div>
                        <button class="w-full py-3 rounded-xl border border-white/20 text-white font-bold hover:bg-white/10 transition-colors">
                            Book Table
                        </button>
                    </div>
                `;
                resultsGrid.appendChild(card);
            });
        } else {
            summaryBox.classList.remove('hidden');
            summaryText.innerHTML = "No restaurants match your criteria. Try broadening your location, cuisine, or rating thresholds.";
            resultsGrid.innerHTML = `
                <div class="col-span-full flex flex-col items-center justify-center p-12 glass-panel rounded-3xl">
                    <span class="material-symbols-outlined text-6xl text-on-surface-variant mb-4" data-icon="search_off">search_off</span>
                    <h3 class="text-xl font-bold text-white mb-2">No Matches Found</h3>
                    <p class="text-on-surface-variant text-center max-w-md">We couldn't find any restaurants that perfectly match your highly specific taste. Try lowering the minimum rating or changing the budget.</p>
                </div>
            `;
        }
    }
});
