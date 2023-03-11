


function formatDisplayeData(data,timeRange){
    let new_datasets = []
    const dataset_length = data.labels.length
    let labels = data.labels.slice(dataset_length-timeRange-1,dataset_length)
    for (var i = 0; i < data.datasets.length; i++){
      let dataset = data.datasets[i].data
      let new_dataset = dataset.slice(dataset_length-timeRange-1,dataset_length)
      new_datasets.push({data:new_dataset,
        label:data.datasets[i].label,
        backgroundColor:data.datasets[i].backgroundColor
        }

      )
    }
    
    return {labels:labels,datasets:new_datasets}

  }

  export default formatDisplayeData;