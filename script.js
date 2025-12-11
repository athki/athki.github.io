// Tab switching functionality and RSS feed fetching
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const tabContents = document.querySelectorAll('.tab-content');

    // Function to switch tabs
    function switchTab(tabName) {
        // Remove active class from all tabs and nav links
        tabContents.forEach(tab => tab.classList.remove('active'));
        navLinks.forEach(link => link.classList.remove('active'));

        // Add active class to selected tab and nav link
        const selectedTab = document.getElementById(tabName);
        const selectedLink = document.querySelector(`[data-tab="${tabName}"]`);
        
        if (selectedTab) selectedTab.classList.add('active');
        if (selectedLink) selectedLink.classList.add('active');
    }

    // Function to fetch and display all writing posts
    async function loadWritingPosts() {
        const postsContainer = document.getElementById('substack-posts');
        if (!postsContainer) return;

        try {
            // Load custom posts from local JSON file
            const customResponse = await fetch('./data/custom-posts.json?v=' + Date.now());
            let customPosts = [];
            
            if (customResponse.ok) {
                const customData = await customResponse.json();
                customPosts = customData.posts || [];
            }

            // Load Substack posts from local JSON file (updated by GitHub Actions)
            const substackResponse = await fetch('./data/substack-posts.json?v=' + Date.now());
            let substackPosts = [];
            
            if (substackResponse.ok) {
                const substackData = await substackResponse.json();
                substackPosts = substackData.posts || [];
            }

            // Combine and sort all posts by date
            const allPosts = [...customPosts, ...substackPosts].sort((a, b) => {
                return new Date(b.pubDate) - new Date(a.pubDate);
            });

            if (allPosts.length === 0) {
                throw new Error('No posts available');
            }

            let postsHTML = '';

            allPosts.forEach(item => {
                // Parse and format the date
                const date = new Date(item.pubDate);
                const formattedDate = date.toLocaleDateString('en-US', { 
                    year: 'numeric', 
                    month: 'long', 
                    day: 'numeric' 
                });

                // Clean up description (remove HTML tags and limit length)
                const cleanDescription = item.description.replace(/<[^>]*>/g, '').substring(0, 150) + '...';

                // Add source indicator
                const sourceBadge = item.source === 'custom' ? '<span class="source-badge">Website</span>' : '<span class="source-badge substack">Substack</span>';

                postsHTML += `
                    <article class="writing-item">
                        <div class="post-header">
                            <h3 class="writing-title">${item.title}</h3>
                            ${sourceBadge}
                        </div>
                        <p class="writing-date">${formattedDate}</p>
                        <p class="writing-excerpt">${cleanDescription}</p>
                        <a href="${item.link}" class="writing-link" target="${item.source === 'custom' ? '_self' : '_blank'}">Read Full Article</a>
                    </article>
                `;
            });

            postsContainer.innerHTML = postsHTML;

        } catch (error) {
            console.error('Error loading writing posts:', error);
            postsContainer.innerHTML = `
                <div class="error-message">
                    <p>Unable to load posts at the moment.</p>
                    <p><a href="https://humanandtheloop.substack.com" target="_blank">Visit my Substack directly</a></p>
                </div>
            `;
        }
    }

    // Add click event listeners to nav links
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tabName = this.getAttribute('data-tab');
            switchTab(tabName);
        });
    });

    // Handle browser back/forward buttons
    window.addEventListener('popstate', function() {
        const hash = window.location.hash.slice(1);
        if (hash) {
            switchTab(hash);
        } else {
            switchTab('home');
        }
    });

    // Initialize with home tab if no hash
    if (!window.location.hash) {
        switchTab('home');
    } else {
        const hash = window.location.hash.slice(1);
        switchTab(hash);
    }

    // Load all writing posts when the page loads
    loadWritingPosts();
}); 