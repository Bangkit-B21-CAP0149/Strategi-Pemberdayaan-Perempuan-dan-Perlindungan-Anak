<template>
  <b-card no-body>
    <b-card-header>
      <div>
        <b-card-title class="mb-1">
          Mentions
        </b-card-title>
        <b-card-sub-title>Mentions Terbaru</b-card-sub-title>
      </div>
    </b-card-header>

    <!-- chart -->
    <b-card-body>
      <app-timeline>
        <app-timeline-item icon="TwitterIcon" v-for="items in item" :key="items.username">
          <div class="d-flex flex-sm-row flex-column flex-wrap justify-content-between mb-1 mb-sm-0">
            <h6>{{ items.user_name }}</h6>
            <small class="text-muted">{{ items.dateLabel }}</small>
          </div>
          <p>{{ items.text.substring(0, 100) + "..." }}</p>
          <div v-if="items.classification_result === 0">
            <b-badge pill variant="danger">Negatif</b-badge>
          </div>
          <div v-else>
            <b-badge pill variant="success">Positif</b-badge>
          </div>
        </app-timeline-item>
      </app-timeline>
    </b-card-body>
  </b-card>
</template>

<script>
import axios from 'axios'
import AppTimeline from '@core/components/app-timeline/AppTimeline.vue'
import AppTimelineItem from '@core/components/app-timeline/AppTimelineItem.vue'
import {
  BBadge, BCard, BCardHeader, BCardBody, BCardSubTitle, BCardTitle,
} from 'bootstrap-vue'

export default {
  components: {
    AppTimeline,
    AppTimelineItem,
    BCard,
    BCardHeader,
    BCardBody,
    BCardSubTitle,
    BCardTitle,
    BBadge,
  },
  data() {
    return {
      item: null,
    }
  },
  created() {
    axios
      .get('http://127.0.0.1:5000/tweet/timeline')
      .then(
        response => {
          this.item = response.data.result
        },
      )
  },
}
</script>
