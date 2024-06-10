var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#vue-span',
  data() {
    return {
      root: root,
      currentQuestion: {},
      userId: document.body.getAttribute('data-user-id') || null,
      problem: {
        milestones: [] // Initialize milestones as an empty array
      },
      problemName: '',
      question: {},
      resource: {},
      activeTab: 'understand',
      isSubmitting: false,
    }
  },
  mounted: async function () {
    this.problemName = problem_name;
    this.fetchProblem();
  },  
  watch: {
    question: function (newQuestion, oldQuestion) {
      this.$nextTick(() => {
        this.initializeSwiper();
      });
    },
  },
  methods: {
    fetchProblem() {
      const problem_name = this.problemName;
      return axios.get(this.root + '/api/problem/?name=' + problem_name)
        .then(response => {
          if (response.data && response.data.length > 0) {
            this.problem = response.data[0]; // Assuming the first item is the desired problem
          } else {
            console.error('No data received from the API.');
          }
        })
        .catch(error => {
          this.message = 'An error occurred while fetching the problem.';
        });
    },
    renderMarkdown(markdownText) {
      return marked.parse(markdownText);
    },
    setActiveTab(tabName) {
      this.activeTab = tabName;
      this.updateQuestionBasedOnTab();
    },
  }
});
