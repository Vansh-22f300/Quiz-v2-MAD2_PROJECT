<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h3 class="text-white">QuizMaster</h3>
        <small class="text-white-50">Admin Panel</small>
      </div>
      <nav class="sidebar-nav">
        <router-link to="/admin" class="nav-link"><i class="fas fa-home me-2"></i>Home</router-link>
        <router-link to="/admin_summary" class="nav-link"><i class="fas fa-chart-bar me-2"></i>Summary</router-link>
        <router-link to="/manage_quiz" class="nav-link"><i class="fas fa-clipboard-list me-2"></i>Manage Quizzes</router-link>
        <router-link to="/admin_user" class="nav-link"><i class="fas fa-users-cog me-2"></i>Manage Users</router-link>
        <router-link to="/manage_subject" class="nav-link active"><i class="fas fa-book me-2"></i>Manage Subjects</router-link>
      </nav>
      <div class="sidebar-footer">
        <router-link to="/login" class="nav-link text-white-50"><i class="fas fa-sign-out-alt me-2"></i>Logout</router-link>
      </div>
    </aside>

    <main class="main-content">
      <header class="content-header">
        <div>
          <h2 class="fw-bold">Manage Subjects</h2>
          <p class="text-muted">Add, edit, and organize subjects and their chapters.</p>
        </div>
        <div class="d-flex align-items-center gap-3">
          <div class="search-wrapper">
            <i class="fas fa-search search-icon"></i>
            <input class="form-control" type="search" placeholder="Search subjects..." v-model="searchQuery" />
          </div>
          <button class="btn btn-primary-custom" @click="addSubjectModal">
            <i class="fas fa-plus me-2"></i>Add Subject
          </button>
        </div>
      </header>

      <section class="mt-4">
        <div v-if="filterSubjects.length === 0" class="alert alert-info">
          No subjects found matching your search.
        </div>

        <div class="accordion" id="subjectsAccordion" v-else>
          <div v-for="(subject) in filterSubjects" :key="subject.id" class="accordion-item">
            <h2 class="accordion-header" :id="'heading' + subject.id">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" :data-bs-target="'#collapse' + subject.id" aria-expanded="false" :aria-controls="'collapse' + subject.id">
                <span class="fw-bold fs-6">{{ subject.name }}</span>
              </button>
            </h2>
            <div :id="'collapse' + subject.id" class="accordion-collapse collapse" :aria-labelledby="'heading' + subject.id" data-bs-parent="#subjectsAccordion">
              <div class="accordion-body">
                <div class="d-flex flex-column flex-sm-row justify-content-between align-items-start gap-2 mb-4">
                  <div>
                    <p class="mb-1"><strong>Description:</strong> {{ subject.description }}</p>
                    <small class="text-muted"><strong>Code:</strong> {{ subject.code }} | <strong>Credits:</strong> {{ subject.credits }}</small>
                  </div>
                  <div class="d-flex flex-wrap gap-2">
                    <button class="btn btn-sm btn-outline-primary" @click="editSubjectModal(subject)"><i class="fas fa-edit me-1"></i> Edit Subject</button>
                    <button class="btn btn-sm btn-outline-danger" @click="deleteSubject(subject.id)"><i class="fas fa-trash me-1"></i> Delete Subject</button>
                  </div>
                </div>

                <h6 class="fw-bold mb-3">Chapters</h6>
                <div class="table-responsive">
                  <table class="table modern-table">
                    <thead>
                      <tr>
                        <th>Chapter Name</th>
                        <th>Description</th>
                        <th class="text-end">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-if="!subject.chapters || subject.chapters.length === 0">
                        <td colspan="3" class="text-center text-muted py-3">No chapters added yet.</td>
                      </tr>
                      <tr v-for="chapter in subject.chapters" :key="chapter.id">
                        <td>{{ chapter.name }}</td>
                        <td>{{ chapter.description }}</td>
                        <td class="text-end">
                          <button class="btn btn-sm btn-outline-secondary me-2" @click="editChapterModal(chapter)"><i class="fas fa-edit"></i></button>
                          <button class="btn btn-sm btn-outline-danger" @click="deleteChapter(chapter.id)"><i class="fas fa-trash"></i></button>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <button class="btn btn-sm btn-accent-custom mt-3" @click="openAddChapterModal(subject.id)">
                  <i class="fas fa-plus me-1"></i>Add Chapter
                </button>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>

     <!-- Add Subject Modal -->
    <div class="modal fade" id="addSubjectModal" tabindex="-1" aria-labelledby="addSubjectModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="addSubjectModalLabel">Add New Subject</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addSubject">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name</label>
                <input type="text" class="form-control" id="subjectName" v-model="newSubject.name" required>
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea class="form-control" id="subjectDescription" v-model="newSubject.description" required></textarea>
              </div>
              <div class="mb-3">
              <label for="subjectCode" class="form-label">Code</label>
              <input type="text" class="form-control" id="subjectCode" v-model="newSubject.code" required>
              </div>
              <div class="mb-3">
                <label for="subjectCredits" class="form-label">Credits</label>
                <input type="number" class="form-control" id="subjectCredits" v-model="newSubject.credits" required>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Add Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Edit Subject Modal -->
    <div class="modal fade" id="editSubjectModal" tabindex="-1" aria-labelledby="editSubjectModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="editSubjectModalLabel">Edit Subject</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editSubject">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name</label>
                <input type="text" class="form-control" id="subjectName" v-model="selectedSubject.name" required>
              </div>
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea class="form-control" id="subjectDescription" v-model="selectedSubject.description" required></textarea>
              </div>
              <div class="mb-3">
              <label for="subjectCode" class="form-label">Code</label>
              <input type="text" class="form-control" id="subjectCode" v-model="selectedSubject.code" required>
              </div>
              <div class="mb-3">
                <label for="subjectCredits" class="form-label">Credits</label>
                <input type="number" class="form-control" id="subjectCredits" v-model="selectedSubject.credits" required>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Edit Subject</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
    <!-- Edit Chapter Modal -->
    <div class="modal fade" id="editChapterModal" tabindex="-1" aria-labelledby="editChapterModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title" id="editChapterModalLabel">Edit Chapter</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="editChapter">
              <div class="mb-3">
                <label for="chapterName" class="form-label">Chapter Name</label>
                <input type="text" class="form-control" id="chapterName" v-model="selectedChapter.name" required>
              </div>
              <div class="mb-3">
                <label for="chapterDescription" class="form-label">Description</label>
                <textarea class="form-control" id="chapterDescription" v-model="selectedChapter.description" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary">Edit Chapter</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="addChapterModal" tabindex="-1" aria-labelledby="addChapterModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addChapterModalLabel">📘 Add New Chapter</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addChapter">
              <div class="mb-3">
                <label for="chapterName" class="form-label fw-semibold">Chapter Name</label>
                <input v-model="newChapter.name" type="text" class="form-control" id="chapterName" placeholder="Enter chapter name" required />
              </div>
              <div class="mb-3">
                <label for="chapterDescription" class="form-label fw-semibold">Description</label>
                <textarea v-model="newChapter.description" class="form-control" id="chapterDescription" placeholder="Enter chapter description" rows="4" required></textarea>
              </div>
              <div class="d-grid">
                <button type="submit" class="btn btn-primary-custom">➕ Add Chapter</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import * as bootstrap from 'bootstrap';

export default {
  data() {
    return {
      subjects: [],
      searchQuery: '',
      newSubject: {
        name: '',
        description: '',
        code: '',
        credits: ''
      },
      selectedSubject: {
        id: '',
        name: '',
        description: '',
        code: '',
        credits: ''
      },
      selectedChapter: {
        id: '',
        name: '',
        description: ''
      },
      adminName: '',
      newChapter: {
        name: '',
        description: '',
        subject_id: null
      },
      addChapterModalInstance: null
    };
  },
  computed: {
    filterSubjects() {
      return this.subjects.filter(subject =>
        subject.name.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  methods: {
    addSubjectModal() {
      const modal = new bootstrap.Modal(document.getElementById('addSubjectModal'));
      modal.show();
    },
    async addSubject() {
      try {
        const response = await fetch('https://quiz-app-v2-py9b.onrender.com/add_subject/post', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
          },
          body: JSON.stringify({
            name: this.newSubject.name,
            description: this.newSubject.description,
            code: this.newSubject.code,
            credits: this.newSubject.credits
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert('Subject added successfully!');
          this.newSubject.name = '';
          this.newSubject.description = '';
          this.newSubject.code = '';
          this.newSubject.credits = '';
          this.fetchSubjects();
          bootstrap.Modal.getInstance(document.getElementById('addSubjectModal')).hide();
        } else {
          alert('Error: ' + data.message);
        }
      } catch (error) {
        console.error('Error adding subject:', error);
        alert('Failed to add subject.');
      }
    },
    fetchSubjects() {
      fetch('https://quiz-app-v2-py9b.onrender.com/add_subject/get', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
        .then(response => response.json())
        .then(data => {
          console.log("Fetched data:", data);
          this.subjects = data;
        })
        .catch(error => {
          console.error('Error fetching subjects:', error);
        });
    },
    editSubjectModal(subject) {
      this.selectedSubject.id = subject.id;
      this.selectedSubject.name = subject.name;
      this.selectedSubject.description = subject.description;
      this.selectedSubject.code = subject.code;
      this.selectedSubject.credits = subject.credits;

      const modal = new bootstrap.Modal(document.getElementById('editSubjectModal'));
      modal.show();
    },
    editSubject() {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_subject/${this.selectedSubject.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify({
          name: this.selectedSubject.name,
          description: this.selectedSubject.description,
          code: this.selectedSubject.code,
          credits: this.selectedSubject.credits
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          bootstrap.Modal.getInstance(document.getElementById('editSubjectModal')).hide();
          this.fetchSubjects();
        })
        .catch(error => {
          console.error('Error editing subject:', error);
          alert('Failed to edit subject.');
        });
    },
    deleteSubject(id){
      if (confirm('Are you sure you want to delete this subject?')) {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_subject/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchSubjects();
      })
      .catch(error => {
        console.error('Error deleting subject:', error);
        alert('Failed to delete subject.');
      });
    }
    },
    editChapterModal(chapter) {
      this.selectedChapter.id = chapter.id;
      this.selectedChapter.name = chapter.name;
      this.selectedChapter.description = chapter.description;
      const modal = new bootstrap.Modal(document.getElementById('editChapterModal'));
      modal.show();
    },
    editChapter() {
      fetch(`https://quiz-app-v2-py9b.onrender.com/edit_chapter/${this.selectedChapter.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        },
        body: JSON.stringify({
          name: this.selectedChapter.name,
          description: this.selectedChapter.description
        }),
      })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
          bootstrap.Modal.getInstance(document.getElementById('editChapterModal')).hide();
          this.fetchSubjects();
        })
        .catch(error => {
          console.error('Error editing chapter:', error);
          alert('Failed to edit chapter.');
        });
    },
    deleteChapter(id){
      if (confirm('Are you sure you want to delete this chapter?')) {
      fetch(`https://quiz-app-v2-py9b.onrender.com/delete_chapter/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        this.fetchSubjects();
      })
      .catch(error => {
        console.error('Error deleting chapter:', error);
        alert('Failed to delete chapter.');
      });
    }
    },
    async getAdminName() {
    try {
      const res = await fetch('https://quiz-app-v2-py9b.onrender.com/admin/profile', {
        method: 'GET',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
        }
      });
      const data = await res.json();
      if (res.ok) {
        this.adminName = data.username;
      } else {
        console.error(data.message);
      }
    } catch (err) {
      console.error('Error:', err);
    }
  },
  openAddChapterModal(subjectId) {
      this.newChapter.name = '';
      this.newChapter.description = '';
      this.newChapter.subject_id = subjectId;
      this.addChapterModalInstance.show();
    },
    async addChapter() {
      if (!this.newChapter.subject_id) return;
      try {
        const response = await fetch(`https://quiz-app-v2-py9b.onrender.com/add_chapter/${this.newChapter.subject_id}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + localStorage.getItem('admin_token')
          },
          body: JSON.stringify({
            name: this.newChapter.name,
            description: this.newChapter.description
          }),
        });
        const data = await response.json();
        alert(data.message);
        if (response.ok) {
          this.fetchSubjects();
          this.addChapterModalInstance.hide();
        }
      } catch (error) {
        console.error("Error adding chapter:", error);
        alert("Failed to add chapter.");
      }
    }


  },
  mounted() {
    this.fetchSubjects();
    this.getAdminName()
    this.addChapterModalInstance = new bootstrap.Modal(document.getElementById('addChapterModal'));

  }
};
</script>
