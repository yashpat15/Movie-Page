<template>
  <div class="movie-page">
    <div class="container">
      <div class="left-column">
        <div class="poster">
          <img :src="movieData.Poster" :alt="movieData.Title" />
          <div class="streaming-info">
            <a
              href="https://www.hotstar.com/in/movies/guardians-of-the-galaxy-vol-2/1260018295"
              target="_blank"
              class="streaming-button"
            >
              <img
                class="hotstar-logo"
                src="https://media.themoviedb.org/t/p/original/zdTSUEVZFXp3E0EkOMGN99QPVJp.jpg"
                alt="Hotstar"
              />
              <div class="streaming-text">
                Now Streaming <span>Watch Now</span>
              </div>
            </a>
          </div>
        </div>
      </div>

      <div class="right-column">
        <h1 class="movie-title">{{ movieData.Title }} ({{ movieData.Year }})</h1>
        <p class="meta-info">
          {{ movieData.Rated }} • {{ movieData.Released }} • {{ movieData.Genre }} • {{ movieData.Runtime }}
        </p>
        <div class="user-score">
  <a href="https://www.imdb.com/title/tt3896198/" target="_blank">
    <img
      class="imdb-logo"
      src="https://upload.wikimedia.org/wikipedia/commons/6/69/IMDB_Logo_2016.svg"
      alt="IMDb Logo"
    />
  </a>
  <div class="score-text">{{ movieData.imdbRating }}/10</div>
  <div class="reaction-share">
    <div class="reaction-section">
      <span @click="likeMovie" class="reaction">👍</span>
      <span @click="dislikeMovie" class="reaction">👎</span>
    </div>
    <div class="share-section">
      <button @click="toggleShareOptions" class="share-icon">🔗</button>
      <div v-if="showShareOptions" class="share-popup">
        <button @click="share('facebook')" class="share-btn">
          <img src="https://upload.wikimedia.org/wikipedia/commons/c/c2/F_icon.svg" alt="Facebook" class="share-logo" />
        </button>
        <button @click="share('twitter')" class="share-btn">
          <img src="https://upload.wikimedia.org/wikipedia/commons/6/6f/Logo_of_Twitter.svg" alt="Twitter" class="share-logo" />
        </button>
        <button @click="share('reddit')" class="share-btn">
          <img src="https://seeklogo.com/images/R/reddit-logo-23F13F6A6A-seeklogo.com.png" alt="Reddit" class="share-logo" />
        </button>
        <button @click="share('gmail')" class="share-btn">
          <img src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Gmail_Icon.png" alt="Gmail" class="share-logo" />
        </button>
      </div>
    </div>
  </div>
</div>

        <p class="overview"><strong>Overview:</strong> {{ movieData.Plot }}</p>
        <p><strong>Director:</strong> {{ movieData.Director }}</p>
        <p><strong>Actors:</strong> {{ movieData.Actors }}</p>
        <p><strong>Writer:</strong> {{ movieData.Writer }}</p>
        <div class="actions">
          <button @click="showTrailer" class="action-btn">▶ Play Trailer</button>
          <button @click="addToWatchlist" class="action-btn">+ Add to Watchlist</button>
        </div>
      </div>
    </div>
<!-- YouTube Modal -->
<div v-if="isTrailerVisible" class="modal">
  <div class="modal-content">
    <iframe
      :src="youtubeUrl"
      frameborder="0"
      allow="autoplay; encrypted-media"
      allowfullscreen
    ></iframe>
    <button class="close" @click="closeTrailer">✖</button>
  </div>
</div>

    <!-- Posts Section -->
    <div class="posts-container">
      <h2>Posts</h2>
      <div v-for="post in posts" :key="post.post_id" class="post">
        <h3>{{ post.author }}</h3>
        <p>{{ post.post_text }}</p>
        <small>{{ post.timestamp }}</small>
        <p>Comments ({{ post.comment_count }}):</p>
        <ul>
          <li v-for="comment in post.comments" :key="comment.comment_id">
            {{ comment.author }}: {{ comment.comment_text }}
          </li>
        </ul>
      </div>
      <div v-if="loading" class="loading-indicator">Loading...</div>
    </div>
  </div>
</template>

---

### Script Section:

```javascript
<script>
import axios from "axios";

const API_URL = "http://127.0.0.1:8000/api/posts/"; 
export default {
  name: "MoviePage",
  data() {
    return {
      movieData: {}, 
      posts: [], 
      nextUrl: API_URL, 
      loading: false, 
      showShareOptions: false, 
      isTrailerVisible: false, 
      youtubeUrl: "https://www.youtube.com/embed/wUn05hdkhjM", 
    };
  },
  methods: {
    showTrailer() {
      this.isTrailerVisible = true;
    },
    closeTrailer() {
      this.isTrailerVisible = false;
    },
    addToWatchlist() {
      alert("Movie added to your watchlist!");
    },
    likeMovie() {
      alert("You liked this movie!");
    },
    dislikeMovie() {
      alert("You disliked this movie.");
    },
    toggleShareOptions() {
      this.showShareOptions = !this.showShareOptions;
    },
    share(platform) {
      const url = encodeURIComponent(window.location.href);
      const title = encodeURIComponent(`Check out this movie: ${this.movieData.Title}`);
      let shareUrl = "";

      if (platform === "facebook") {
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${url}`;
      } else if (platform === "twitter") {
        shareUrl = `https://twitter.com/intent/tweet?text=${title}&url=${url}`;
      } else if (platform === "reddit") {
        shareUrl = `https://reddit.com/submit?title=${title}&url=${url}`;
      } else if (platform === "gmail") {
        shareUrl = `mailto:?subject=${title}&body=${url}`;
      }

      window.open(shareUrl, "_blank");
    },

    fetchMovieData() {
      axios
        .get("http://www.omdbapi.com/?i=tt3896198&apikey=d2132124")
        .then((response) => {
          this.movieData = response.data;
        })
        .catch((error) => {
          console.error("Error fetching movie data:", error);
        });
    },

    async fetchPosts() {
      if (!this.nextUrl || this.loading) return;
      this.loading = true;

      try {
        const response = await axios.get(this.nextUrl);
        this.posts.push(...response.data.results); 
        this.nextUrl = response.data.next; 
      } catch (error) {
        console.error("Error fetching posts:", error);
      } finally {
        this.loading = false;
      }
    },

    handleScroll() {
      const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
      const scrollPosition = window.scrollY;

      if (scrollPosition >= scrollableHeight - 200) {
        this.fetchPosts();
      }
    },
  },
  mounted() {
    this.fetchMovieData();
    this.fetchPosts();
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
};
</script>


<style>
body {
  font-family: "Roboto", sans-serif;
  background-color: #0c1b28;
  color: white;
  margin: 0;
}


.left-column {
  flex: 1;
  max-width: 300px;
}

.poster img {
  width: 100%;
  border-radius: 8px;
}

.streaming-info {
  margin-top: 10px;
  text-align: center;
}


.right-column {
  flex: 2;
  padding: 20px;
}

.movie-title {
  font-size: 28px;
  margin-bottom: 10px;
}

.meta-info {
  font-size: 14px;
  margin-bottom: 20px;
  color: #ccc;
}

.user-score {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 20px;
}

.imdb-logo {
  width: 40px;
  height: auto;
}

.score-text {
  font-size: 18px;
  font-weight: bold;
  color: white;
}

.reaction-share {
  display: flex;
  align-items: center;
  gap: 15px;
}

.reaction-section {
  display: flex;
  gap: 8px;
}

.reaction {
  cursor: pointer;
  font-size: 18px;
}

.reaction:hover {
  transform: scale(1.2);
  transition: transform 0.2s;
}

.share-section {
  display: flex;
  align-items: center;
}

.share-icon {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.share-icon:hover {
  transform: scale(1.2);
}

.share-btn {
  background: none;
  border: none;
  padding: 6px 10px;
  cursor: pointer;
}

.share-logo {
  width: 20px;
  height: 20px;
}

.share-btn:hover {
  transform: translateY(-2px);
}

.actions {
  margin-top: 20px;
}

.action-btn {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  margin-right: 10px;
  cursor: pointer;
}

.action-btn:hover {
  background-color: #0056b3;
}

/* Modal Fix */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  position: relative;
  width: 80%;
  max-width: 900px;
}

.modal iframe {
  width: 100%;
  height: 500px;
  border: none;
}

.close {
  position: absolute;
  top: 10px;
  right: 15px;
  font-size: 24px;
  color: white;
  cursor: pointer;
}

.close:hover {
  color: red;
}
.container {
  display: flex;
  flex-wrap: wrap;
  max-width: 1200px;
  margin: auto;
  padding: 20px;
  gap: 20px; 
}


/* Responsive Design for Mobile */
@media screen and (max-width: 768px) {
  .container {
    flex-direction: column;
    align-items: center;
  }

  .left-column, .right-column {
    max-width: 100%;
    text-align: center;
  }

  .movie-title {
    font-size: 20px;
  }

  .meta-info, .score-text {
    font-size: 14px;
  }

  .actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 10px;
  }
}

/* For Larger Tablets */
@media screen and (max-width: 1024px) {
  .container {
    gap: 10px;
    padding: 10px;
  }

  .movie-title {
    font-size: 24px;
  }

  .actions {
    gap: 5px;
  }
}

.streaming-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background-color: #002d62; 
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  width: fit-content; 
  gap: 8px;
}

.streaming-button span {
  font-weight: bold;
  font-size: 14px;
}

.streaming-button img {
  width: 24px; 
  height: 24px;
  border-radius: 4px; 
}



.streaming-button {
  display: flex;
  align-items: center;
  background-color: #002d62; 
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none; 
  gap: 10px;
  width: fit-content;
  margin: auto;
  cursor: pointer;
}

.streaming-button:hover {
  background-color: #004080; 
}

.hotstar-logo {
  width: 32px;
  height: 32px;
  border-radius: 4px;
}

.streaming-text {
  font-size: 14px;
  font-weight: 500;
}

.streaming-text span {
  font-weight: bold;
}

</style>
