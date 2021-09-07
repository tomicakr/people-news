<script>
import { Bar } from "vue-chartjs";

export default {
  extends: Bar,
  props: ['labels', 'counts'],
  mounted() {
    const chartdata = {
      labels: this.labels,
      datasets: [
        {
          label: "Broj pojava imena",
          data: this.counts,
        },
      ],
    };
    const options = {
      responsive: true,
      maintainAspectRatio: false,
    };
    this.renderChart(chartdata, options);
  },
};
</script>

<style>
</style>