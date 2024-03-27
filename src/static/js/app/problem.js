var app = new Vue({
  delimiters: ['[[', ']]'],
  el: '#vue-span',
  data() {
    return {
      root: root,
      problem: {
        milestones: [] // Initialize milestones as an empty array
      },
      question: {},
      resource: {},
      activeTab: 'understand',
    }
  },
  watch: {
    question: function(newQuestion, oldQuestion) {
      this.$nextTick(() => {
        this.initializeSwiper();
      });
    }
  },
  mounted: async function() {
    await this.fetchProblem();
    this.setActiveTab(this.activeTab);
  },
  methods: {
    renderMarkdown(markdownText) {
      return marked.parse(markdownText);
    },
    setActiveTab(tabName) {
      this.activeTab = tabName;
      // Ensure 'problem' and 'problem.questions' are defined before accessing
      if (this.problem && this.problem.questions && this.problem.questions[tabName]) {
        this.question = this.problem.questions[tabName];
      } else {
        this.question = [];
      }
    },
    fetchProblem() {
      return axios.get(this.root + '/api/problem/?name=' + problem_name)
        .then(response => {
          if (response.data && response.data.length > 0) {
            this.problem = response.data[0];
          } else {
            this.message = 'An error occurred while fetching the problem.';
          }
        })
        .catch(error => {
          console.error("There was an error fetching the problem:", error);
          this.message = 'An error occurred while fetching the problem.';
        });
    },
    initializeSwiper() {
      if (this.swiperInstance) {
        this.swiperInstance.destroy();
      }
      this.$nextTick(() => {
        this.swiperInstance = new Swiper('.swiper-container', {
          slidesPerView: 1,
          pagination: {
            el: '.swiper-pagination',
            clickable: true,
          },
        });
      });
    },
  }
});
