<template>
  <div class="form form-modern search">
    <sg-input type="search" v-model="searchTerm" label="Gruppen suchen..."
              :groupClasses="{'search-loading': isSearching }"
              :inputClasses="['search-input']"></sg-input>
    <div v-if="!searchTerm" v-html="defaultResults"></div>
    <div class="search-results" v-else-if="hasResults">
      <group-preview :group="group" :key="group.id" v-for="group in results" />
    </div>
    <div v-else-if="hasNoResults">
      <div class="alert alert-block">Nix g’scheites bei 😞</div>
    </div>
  </div>
</template>

<script>
  import { debounce } from 'lodash'
  import axios from 'axios'
  import { group } from '../../adapters/api'
  import { danger } from '../../util/notify'
  import GroupPreview from './group-mini-preview.vue'

  export default {
    components: { GroupPreview },
    props: {
      defaultResults: String
    },
    data () {
      return {
        searchTerm: '',
        searchToken: null,
        results: []
      }
    },
    computed: {
      isSearching () {
        return this.searchToken !== null && this.searchToken !== 'pending'
      },
      hasNoResults () {
        return this.searchToken === null && this.searchTerm && this.results.length === 0
      },
      hasResults () {
        return this.searchToken === null && this.searchTerm && this.results.length > 0
      }
    },
    watch: {
      searchTerm: [
        function () { this.searchToken = 'pending' },
        debounce(function (value) {
          if (this.searchToken && this.searchToken.cancel) {
            this.searchToken.cancel('new_request')
          }

          if (!this.searchTerm.trim()) {
            this.searchToken = null
            return
          }

          const token = this.searchToken = axios.CancelToken.source()
          this.results = []
          group.list({ name: value }, {
            cancelToken: token.token
          }).then(
            res => {
              this.searchToken = null
              this.results = res.data.slice(0, 3)
            },
            err => {
              this.searchToken = null
              if (!axios.isCancel(err)) {
                console.error(err)
                danger('Bei der Suchanfrage ist ein Fehler aufgetreten')
              }
            }
          )
        }, 300)
      ]
    }
  }
</script>
