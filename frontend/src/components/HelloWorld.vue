<template>
  <div>
    <nav class="navbar navbar-expand-lg navbar-light bg-white shadow-sm py-3 sticky-top">
      <div class="container">
        <a class="navbar-brand fw-bold fs-3" href="#" style="color: #4F46E5;">QuizMaster</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto align-items-center">
            <li class="nav-item"><a class="nav-link active fw-semibold" href="#">Home</a></li>
            <li class="nav-item"><a class="nav-link fw-semibold" href="#">Features</a></li>
            <li class="nav-item"><router-link class="nav-link fw-semibold" to="/login">Login</router-link></li>
            <li class="nav-item ms-lg-2 mt-2 mt-lg-0">
              <router-link class="btn btn-primary-custom fw-semibold" to="/signup">Sign Up</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    <header class="hero-section d-flex align-items-center text-center text-lg-start">
  <div class="container">
    <div class="row">
      <div class="col-lg-8"> <h1 class="display-3 fw-bold text-white">Ace Your Quizzes with Confidence!</h1>
        <p class="lead my-4">Practice, progress and perform better — all in one place.</p>
        <div class="d-flex flex-column flex-sm-row align-items-center gap-3 justify-content-center justify-content-lg-start">
          <router-link to="/login" class="btn btn-accent-custom btn-lg">Start Now</router-link>
          <router-link to="/signup" class="btn btn-outline-light btn-lg">Join Free</router-link>
        </div>
      </div>
    </div>
  </div>
    </header>

    <main class="container py-5 mt-4">
      <section class="text-center">
        <h2 class="fw-bold">Features That Set Us Apart</h2>
        <p class="text-muted mb-5">Everything you need to grow smarter.</p>
        <div class="row g-4">
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow feature-card p-4">
              <div class="feature-icon mx-auto mb-4"><i class="bi bi-lightbulb-fill"></i></div>
              <h5 class="fw-bold">Smart Questions</h5>
              <p class="text-muted">Dynamic quizzes tailored to your level, curated by subject experts.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow feature-card p-4">
              <div class="feature-icon mx-auto mb-4"><i class="bi bi-graph-up-arrow"></i></div>
              <h5 class="fw-bold">Track Progress</h5>
              <p class="text-muted">Analyze your results and see improvements over time with detailed reports.</p>
            </div>
          </div>
          <div class="col-md-4">
            <div class="card h-100 border-0 shadow feature-card p-4">
              <div class="feature-icon mx-auto mb-4"><i class="bi bi-trophy-fill"></i></div>
              <h5 class="fw-bold">Rewards & Ranks</h5>
              <p class="text-muted">Earn badges and climb leaderboards as you complete milestones.</p>
            </div>
          </div>
        </div>
      </section>

      <section class="cta-section text-white text-center p-5 mt-5">
          <h2 class="fw-bold mb-3">Join 50,000+ learners mastering their skills</h2>
          <p class="lead mb-4">Start your learning journey with QuizMaster today!</p>
          <router-link to="/signup" class="btn btn-light btn-lg px-4 fw-semibold">Create Free Account</router-link>
      </section>
    </main>

    <footer class="app-footer text-white text-center py-4 mt-5">
      <div class="container">
        <small>&copy; 2025 QuizMaster. All rights reserved.</small>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'LandingPage',
}
</script>