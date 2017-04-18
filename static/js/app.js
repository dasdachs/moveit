var vm = new Vue({
  delimiters: ["[[", "]]"],
  el: "#app",
  data: {
    movements: [],
  },
  computed: { 
    parsedDates: function() {
      return this.formatDates("readable");
    },
  },
  methods: {
    addMovement: function() {
      this.movements.push(moment())
    },
    removeMovement: function(index) {
      this.movements.splice(index, 1)
    },
    formatDates: function(format) {
      if (format === "readable") {
        // pushes MomentJs objects to array movements
        // the array movement is than computed to a
        // friendlier format
        return this.movements.map(function(date) {
          return date.format('MMMM Do YYYY, h:mm:ss');
        })
      } else {
        // return an array with ISO8601 strings
        return this.movements.map(function(date) {
          return date.toISOString();
        })
      }
    },
    sendData: function() {
      axios({
        method: "post",
        url: "/add-movement",
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "contentType": "application/json"
        },
        data: {
          moves: this.formatDates(),
        }
      })
      .then(
        // we use splice since splice is
        // a change that VueJS watches
        this.movements.splice(0, this.movements.length)
      )
      .catch(function(error) {
        console.log(error);
      })
    }
  }
})
