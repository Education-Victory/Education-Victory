var app = new Vue({
      delimiters: ['[[', ']]'],
      el: '#vue-span',
      data () {
        return {
           root: root,
           problem: [],
           all_question: {},
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
      mounted () {
        this.fetchProblem();
        this.fetchQuestion();
        this.fetchSubmission();
      },
      methods: {
        setActiveTab(tabName) {
            this.activeTab = tabName;
            this.question = this.all_question[this.activeTab] || [];
        },
        initializeSwiper() {
          if (this.swiperInstance) {
            this.swiperInstance.destroy();
          }
          this.$nextTick(() => {
            this.swiperInstance = new Swiper('.swiper-container', {
              slidesPerView: 1,
              autoHeight: true,
              pagination: {
                el: '.swiper-pagination',
                clickable: true, // Ensure pagination is clickable
              },
            });
          });
        },
        submitAnswer(questionId, questionType, isCorrect, content) {
          axios.post('/api/submission/submit-answer/', {
            question_id: questionId,
            question_type: questionType,
            correct: isCorrect,
            content: content
          }, {
            headers: {
              'X-CSRFToken': csrfToken // Add CSRF token here
            }
          })
          .then(response => {
            console.log("Answer submitted successfully.");
              // Handle any further actions after submission, like updating UI
          })
          .catch(error => {
            console.error("Error submitting answer:", error);
          });
        },
        toggleChoice(questionIndex, choiceIndex) {
          const question = this.question[questionIndex];
          // Keep track of selected indices
          let selectedSet = new Set();
          question.userChoices.forEach((selected, index) => {
            if (selected) {
              selectedSet.add(index);
            }
          });

          // Determine correctness
          let isCorrect = true;
          let hasIncorrectSelection = false;

          // Check if all selected choices are correct
          selectedSet.forEach(index => {
            if (!question.answerSet.has(index)) {
              hasIncorrectSelection = true;
            }
          });

          // Check if all correct choices are selected
          question.answerSet.forEach(index => {
            if (!selectedSet.has(index)) {
              isCorrect = false;
            }
          });

          // Update the question state based on correctness
          Vue.set(question, 'isCorrect', isCorrect && !hasIncorrectSelection);
          Vue.set(question, 'isIncorrect', hasIncorrectSelection);


          if (hasIncorrectSelection | (isCorrect && !hasIncorrectSelection)) {
            const questionId = this.question[questionIndex].id;
            const questionType = 'choice'; // Or 'coding', depending on your logic
            const content = JSON.stringify(this.question[questionIndex].userChoices); // Adjust according to what you want to send
            this.submitAnswer(questionId, questionType, question.isCorrect, content);
          }
        },
        fetchQuestion() {
          axios.get(root + '/api/question/?name='  + problem_name)
            .then(response => {
              this.all_question = response.data;
              Object.keys(this.all_question).forEach((category) => {
                this.all_question[category].forEach((question) => {
                  Vue.set(question, 'show_explanation', false);
                  Vue.set(question, 'userChoices', new Array(question.desc.choice.length).fill(false));
                  const binaryAnswer = question.answer.toString(2).padStart(question.desc.choice.length, '0').split('').reverse();
                  const answerSet = new Set();
                  binaryAnswer.forEach((bit, index) => {
                    if (bit === '1') {
                      answerSet.add(index);
                    }
                  });
                  Vue.set(question, 'answerSet', answerSet);
                  Vue.set(question, 'isCorrect', false); // Assuming default is false
                  Vue.set(question, 'isIncorrect', false); // Assuming default is false
                });
              });
              this.question = this.all_question[this.activeTab];
            })
            .catch(error => {
              console.error('An error occurred while fetching the questions:', error);
              this.message = 'An error occurred while fetching the problem.';
            });
        },
        fetchSubmission() {
          axios.get(root + '/api/submission/?name='  + problem_name + '&type=' + this.activeTab)
            .then(response => {
              // Handle the response, e.g., storing it in your Vue component's data
              this.submissions = response.data;
            })
            .catch(error => {
              console.error('An error occurred while fetching the submissions:', error);
            });
        },
        fetchProblem() {
          axios.get(root + '/api/problem/?name=' + problem_name)
            .then(response => {
                if (response.data && response.data.length > 0) {
                    this.problem = response.data[0];
                } else {
                    this.message = 'An error occurred while fetching the problem.';
                }
            })
            .catch(error => {
                this.message = 'An error occurred while fetching the problem.';
            });
          },
        },
      computed: {
        filteredMilestones() {
          if (!this.problem.milestone_detail) {
            return [];
          }
          return this.problem.milestone_detail.filter(milestone => milestone.type === this.activeTab);
        }
      }
    })
