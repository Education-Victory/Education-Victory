var app = new Vue({
      delimiters: ['[[', ']]'],
      el: '#vue-span',
      data () {
        return {
           root: root,
           problem: [],
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
      },
      methods: {
        renderMarkdown(markdownText) {
          return marked.parse(markdownText);
        },
        setActiveTab(tabName) {
            this.activeTab = tabName;
            this.question = this.problem.questions[this.activeTab] || [];
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
                clickable: true, // Ensure pagination is clickable
              },
            });
          });
        },
        updateQuestionsWithSubmission() {
            this.fetchSubmission().then(() => {
              this.submission.forEach(sub => {
                for (let category in this.all_question) {
                  const questionIndex = this.all_question[category].findIndex(
                    q => q.name === sub.question_name
                  );
                  // If a matching question is found
                  if (questionIndex !== -1) {
                    const question = this.all_question[category][questionIndex];
                    const userChoices = JSON.parse(sub.content);

                    Vue.set(question, 'userChoices', userChoices);
                    Vue.set(question, 'isCorrect', sub.correct);
                    Vue.set(question, 'isIncorrect', !sub.correct);
                    Vue.set(question, 'disabled', true);
                  }
                }
              });
            });
          },
        resetQuestion(i) {
          const question = this.question[i];
          Vue.set(question, 'userChoices', new Array(question.desc.choice.length).fill(false));
          Vue.set(question, 'isCorrect', false);
          Vue.set(question, 'isIncorrect', false);
          Vue.set(question, 'disabled', false);
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
          Vue.set(question, 'disabled', question.isCorrect || question.isIncorrect);

          if (hasIncorrectSelection | (isCorrect && !hasIncorrectSelection)) {
            const questionId = this.question[questionIndex].id;
            const questionType = 'choice'; // Or 'coding', depending on your logic
            const content = JSON.stringify(this.question[questionIndex].userChoices); // Adjust according to what you want to send
            this.submitAnswer(questionId, questionType, question.isCorrect, content);
          }
        },
        fetchSubmission() {
          return axios.get(root + '/api/submission/?name='  + problem_name + '&type=' + this.activeTab)
            .then(response => {
              // Handle the response, e.g., storing it in your Vue component's data
              this.submission = response.data;
            })
            .catch(error => {
              console.error('An error occurred while fetching the submissions:', error);
            });
        },
        fetchProblem() {
          return axios.get(root + '/api/problem/?name=' + problem_name)
            .then(response => {
                if (response.data && response.data.length > 0) {
                    this.problem = response.data.problems;
                    if (this.problem.questions && this.problem.questions[this.activeTab]) {
                        this.question = this.problem.questions[this.activeTab];
                    } else {
                        // Handle the case where questions are not available
                        this.question = [];
                    }
                } else {
                    this.message = 'An error occurred while fetching the problem.';
                }
            })
        },
        findQuestionByName(questionName) {
          for (let category in this.all_question) {
            const question = this.all_question[category].find(q => q.name === questionName);
            if (question) {
              return question;
            }
          }
          return null;
        }
      },
      computed: {
        filteredMilestones() {
          if (!this.problem.milestone_detail) {
            return [];
          }
          return this.problem.milestone_detail.filter(milestone => milestone.type === this.activeTab);
        },
         milestoneCompletionStatus() {
            let completionStatus = {};
            this.problem.milestone_detail.forEach(milestone => {
              // Initially assume all questions under the milestone are correct
              let allCorrect = true;
              // Check each question related to the milestone
              milestone.question.forEach(question => {
                const questionInAllQuestions = this.findQuestionByName(question.name);
                if (!questionInAllQuestions || !questionInAllQuestions.isCorrect) {
                  allCorrect = false;
                }
              });
              // Set the completion status for the milestone
              completionStatus[milestone.id] = allCorrect;
            });
            return completionStatus;
        }
      }
    })
