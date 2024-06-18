
let map, popup
const sas_token = '?sv=2023-01-03&st=2024-05-30T13%3A20%3A12Z&se=2024-12-31T14%3A20%3A00Z&sr=c&sp=r&sig=P3AjEjL3Whum1eGMEElzWP1OB2nKrrKJGK9PaqozEJA%3D'
const bloburl = 'https://rrfimainstorage.blob.core.windows.net/rrfimaincon/'
const mapsSubsKey = 'hbEt0GgOUF-cxXIii9kk5L3rA2yO1SvHzlSk_lT08Jk'
const addressSubsKey = '1LnrhfcdFVeuJ7jVOe2ElJi2uFib34RZhLWnig1nDiAzSeAIlOEO'
const index = 'rrfisearch_v2' //'rrfimaingis'// 'rrfiworddoc'//'rrfiexcelsheets' //rrfisearch
const searchURL = `https://rrfimainsearch.search.windows.net/indexes/${index}/docs/search?api-version=2023-11-01`
const geocodeUrl = `https://atlas.microsoft.com/search/address/json?subscription-key=${mapsSubsKey}&api-version=1.0&query=`
const fileUploadUrl = "https://rrfimainfuncapp.azurewebsites.net/api/generate_upload_sas?code=xC1M9juxwgrDkeMgLrmb7H_oAjs1VeFQxNorPlIvZIb9AzFulOxnIw%3D%3D"
let searchRecords = []
let uniqueHashValues = []
let topCount = 50
let skipCount = 0
let duplicates = 0
// Mapping of Area_Name values to colors
let areaColors = {
    "THM": "DodgerBlue",
    "CLA": "Green",
    "WMD": "Red",
    // Add more mappings as needed
}
let searchedPostcodes = {}
let username

function getMap() {
    openLoginModal()
    // Initialize Azure Maps
    console.log("Initializing Azure Maps...")
    map = new atlas.Map('map', {
        center: [-2.2426, 54.3833], // Center coordinates of the United Kingdom
        zoom: 4, // Zoom level to show the entire country
        view: 'Auto',
        authOptions: {
            authType: 'subscriptionKey',
            subscriptionKey: mapsSubsKey
        }
    })

    popup = new atlas.Popup({
        //content: popupContent
        pixelOffset: [0, -18]
    })

    //Wait until the map resources are ready.
    map.events.add('ready', function () {
        //Optional. Add the map style control so we can see how the custom control reacts.
        map.controls.add([
            new atlas.control.StyleControl(),
            new atlas.control.ZoomControl(),
            //Add the custom control to the map.
            new atlas.control.FullscreenControl({
                style: 'auto'
            })
        ], {
            position: 'top-right'
        })
    })
    //createSearchRequest()
    htmlSupportEvents()
}

function clearUI() {
    searchedPostcodes = {}
    searchRecords = []
    uniqueHashValues = []
    map.markers.clear()
    $('#listViewContainer').empty()
    $('#res-count').text('')
    skipCount = 0
    duplicates = 0
}

let requestBody = {}
function createSearchRequest() {
    clearUI()
    let searchkey = $('#txt-search').val()
    //let searchfilter = $('#select-filter').val()
    if (searchkey?.length == 0) {
        return false
    }
    // Construct POST request body
    requestBody = {
        "search": "*",
        "count": true,
        "searchMode": "all",
        "top": topCount,
        "skip": skipCount
        //"filter": "Geo_Tag eq 'Y'",
        //"filter": "Area_Name eq '"+searchkey+"'"
    }

    let filter = processFilter()
    if (filter?.length > 0) {
        requestBody['filter'] = filter
    }
    // if(searchfilter == 'area') {
    //     requestBody['filter'] = "Area_Name eq '"+searchkey+"'"
    // } else if(searchfilter == 'postcode') {
    //     //requestBody['filter'] = "Postcode eq '"+searchkey+"'"
    //     requestBody['filter'] = `contains(Postcode,'${searchkey}')`
    // } else {
    requestBody['search'] = searchkey
    //}
    $('.spinner-container').show()
    searchData(requestBody)
}

function loadMoreResults() {
    $('.spinner-container').show()
    skipCount = requestBody['skip'] + topCount
    requestBody['skip'] = skipCount
    searchData(requestBody)
}

function processFilter() {
    const propFlooded = $('#selectPropFlooded').val()
    const propProtected = $('#selectPropProtected').val()
    const securityClass = $('#selectSecurityClass').val()

    const filter = []
    if (propFlooded != 'Any') {
        filter.push(`Properties_Flooded eq '${propFlooded}'`)
    }
    if (propProtected != 'Any') {
        filter.push(`Property_Protected eq '${propProtected}'`)
    }
    if (securityClass != 'Any') {
        filter.push(`Security_Classification eq '${securityClass}'`)
    }
    if (filter?.length > 0) {
        $('#btnSearchFilter span').text(`(${filter.length})`);
    } else {
        $('#btnSearchFilter span').text('');
    }
    return filter.join(' and ')
}

function searchData(requestBody) {
    // Perform POST request to Azure Cognitive Search API
    console.log("Fetching search results from Azure Cognitive Search API...")
    fetch(searchURL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'api-key': addressSubsKey
        },
        body: JSON.stringify(requestBody)
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch search results. Status: ' + response.status)
            }
            return response.json()
        })
        .then(data => {
            //console.log("Search results received:", data)

            let geotaggedCount = 0
            searchRecords = [...searchRecords, ...data.value]
            // Process search results and add markers and pop-ups to the map
            if (searchRecords?.length >= data["@odata.count"]) {
                $('#divViewMore').css('visibility', 'hidden');
            } else {
                $('#divViewMore').css('visibility', 'visible');
            }
            data.value.forEach((result, index) => {
                if (!isDuplicate(result)) {
                    createListView(result, skipCount + index)
                    showMarker(result)
                    uniqueHashValues.push(result.Hash_Value)
                    if (result.Geo_Tag == 'Y') {
                        geotaggedCount++
                    }
                } else {
                    console.log('Skipping for duplicate', result.File_Name, result)
                    duplicates++
                }
            })
            let resText = `Showing ${((skipCount+topCount) > data["@odata.count"]) ? data["@odata.count"] : skipCount+topCount } of ${data["@odata.count"]}`
            let resAllText = `Total Results: ${data["@odata.count"]}`
            if (duplicates > 0) {
                resAllText += ` | Duplicates : ${duplicates}`
            }
            $('#res-count').text(resText)
            $('#res-all-count').text(resAllText)
            //+ " || Geotagged results: "+ geotaggedCount)
            $('.spinner-container').hide()
        })
        .catch(error => {
            console.error('Error fetching or processing search results:', error.message)
            $('.spinner-container').hide()
        })
}

function isDuplicate(result) {
    return (uniqueHashValues.indexOf(result.Hash_Value) > -1)
}

function showMarker(result) {
    // Check if latitude and longitude are not null
    if (result.Latitude !== null && result.Longitude !== null) {
        //console.log("Processing result:", result)

        let latitude = result.Latitude // Access latitude from search result
        let longitude = result.Longitude // Access longitude from search result

        let areaName = result.Area_Name || '' // Access Area_Name from search result
        let markerColor = areaColors[areaName] || 'DodgerBlue' // Get color based on Area_Name, default to 'DodgerBlue'

        let marker = getMarker(longitude, latitude)

        let popupContent = getPopupContent(result)

        // Attach click event listener to the marker
        marker.getElement().addEventListener('click', function () {
            popup.setOptions({
                position: [longitude, latitude],
                content: popupContent
            })
            popup.open(map)
        })

        // Add the marker to the map
        map.markers.add(marker)
    } else {
        processPostcodes(result)
    }
}

function getPopupContent(result, postcode = null) {
    let pc = []
    if (!postcode) pc.push('<div><img class="popup-img" src="' + (bloburl + result.File_Path + sas_token) + '"></div>')
    pc.push('<div><strong>Incident Name:</strong> <span class="p-val">' + (result.Incident_Name || '') + '</span></div>')
    pc.push('<div><strong>Area Name:</strong> <span class="p-val">' + (result.Area_Name || '') + '</span></div>')
    pc.push('<div><strong>Incident Date and Time:</strong> <span class="p-val">' + (result.Incident_Date_and_Time || '') + '</span></div>')
    if (postcode) pc.push('<div><strong>Postcode:</strong> ' + (postcode || '') + '</div>')
    pc.push('<div><strong>File Name:</strong> <span class="p-val">' + (result.File_Name || '') + '</span></div>')
    pc.push('<div class="border-bottom"><strong>File Path:</strong> <span class="p-val">' + (result.Source_Path || '') + '</span></div>')
    return pc.join('')
}

function processPostcodes(result) {
    // Check if Postcode is not null and is a string
    if (typeof result.Postcode === 'string' && result.Postcode.trim() !== '') {
        //console.log("Processing Postcode result:", result)

        // Split the Postcode string into individual Postcode values
        var postcodes = result.Postcode.split(',').map(function (postcode) {
            return postcode.trim() // Remove leading and trailing spaces
        })

        // Iterate over each Postcode value
        postcodes.forEach(function (postcode) {
            if (searchedPostcodes[postcode]) {
                processPostcodePopupContent(result, postcode)
                return false
            }
            // Use a geocoding service to get latitude and longitude for the Postcode
            fetch(`${geocodeUrl}${postcode}, UK`)
                .then(response => response.json())
                .then(geocodeData => {
                    if(geocodeData.results[0].matchConfidence.score < 0.9) {
                        return false;
                    }
                    var coordinates = geocodeData.results[0].position
                    var latitude = coordinates.lat
                    var longitude = coordinates.lon

                    // Create a marker for the Postcode location
                    var marker = getMarker(longitude, latitude)

                    // Construct popup content
                    processPostcodePopupContent(result, postcode)
                    //searchedPostcodes[postcode] = popupContent

                    // Attach click event listener to the marker to open the popup
                    marker.getElement().addEventListener('click', function () {
                        popup.setOptions({
                            position: [longitude, latitude],
                            content: searchedPostcodes[postcode]
                        })
                        popup.open(map)
                    })

                    // Add the marker to the map
                    map.markers.add(marker)

                })
                .catch(error => {
                    console.error('Error geocoding Postcode:', error.message)
                })
        })
    }
}

function processPostcodePopupContent(result, postcode) {
    // Construct popup content
    var popupContent = getPopupContent(result, postcode)
    searchedPostcodes[postcode] = (searchedPostcodes[postcode]) ? searchedPostcodes[postcode] + popupContent : popupContent
}

function getMarker(longitude, latitude) {
    return new atlas.HtmlMarker({
        position: [longitude, latitude],
        htmlContent: atlas.getImageTemplate("pin"), // Document icon
        color: 'red' // Marker color set to grey
    })
}

function createListView(rowData, index) {
    divEl = $('#listViewContainer')
    let props = []
    props.push(`<p class="m-0"><strong>Incident Name:</strong> ${rowData.Incident_Name}</p>`)
    props.push(`<p class="m-0"><strong>Incident Date:</strong> ${rowData.Incident_Date_and_Time}</p>`)
    //props.push("Incident Name:"+rowData.Incident_Name)
    props.push(`<p class="m-0"><strong>File Name:</strong> ${rowData.File_Name}</p>`)
    props.push(`<p class="m-0"><strong>River Name:</strong> ${rowData.River_Name}</p>`)
    props.push(`<p class="m-0"><strong>Source Name:</strong> ${rowData.Source_Name}</p>`)
    props.push(`<p class="m-0"><strong>File Path:</strong> ${getFilePath(rowData)}</p>`)
    props.push(`<p class="m-0"><strong>Area Name:</strong> ${rowData.Area_Name}</p>`)
    props.push(`<p class="m-0"><strong>Postcode:</strong> ${rowData.Postcode}</p>`)
    //props.push("<strong>File Hash:</strong> " + rowData.Hash_Value)
    let security_class = `<td><mark>${getSecurityClass(rowData)}</mark></td>`
    let open_details = getOpenDetailsHTML(index)
    let html = `<tr><td>${props.join('')}</td>${open_details}${security_class}</tr>`
    divEl.append(html)
}

function getSecurityClass(rowData) {
    return (rowData?.Security_Classification?.length < 15 && (rowData?.Security_Classification?.indexOf('Official') > -1
        || rowData?.Security_Classification?.indexOf('Secret') > -1)) ? rowData.Security_Classification : '--'
}

function getFilePath(rowData) {
    rowData.File_Path = rowData.File_Path.replaceAll("'","%27")
    if(username == 'internaluser' && (rowData?.Security_Classification == 'Top Secret' || rowData?.Security_Classification == 'Secret')) {
        return rowData.File_Path
    } else {
        const link = `${(rowData.File_Path.indexOf('http') !=0 ) ? bloburl : ''}${rowData.File_Path}${(rowData.File_Path.indexOf(rowData.File_Name) < 0) ? '/'+rowData.File_Name : ''}`
        return `<a href="#" class="text-break link-dark link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" title="View record details" onclick="openDocLink('${link}')">
        ${link}
        </a>`
    }
}

function openDocLink(link) {
    window.open(link + sas_token, '_blank')
}

function getOpenDetailsHTML(index) {
    return `<td>
                <a href="#" class=" fs-5 link-dark link-offset-2 link-underline-opacity-25 link-underline-opacity-100-hover" title="View record details" onClick="viewDetailedInfo('${index}')">
                <i class="bi bi-card-list"></i>
                </a>
            </td>`
}

function viewDetailedInfo(index) {
    const record = searchRecords[index]
    const html = []
    for (const prop in record) {
        if (prop == '@search.score' || prop == 'id') {
            continue;
        }
        const colName = prop.replace(/_/g, " ")
        html.push(`<p><strong>${colName}</strong> : ${record[prop]}</p>`)
    }
    $('#recordInfo').html(html.join(''))
    $('#recordInfoModal').modal('show')
    $('#txtRecordInfo').text(searchRecords[index].File_Name)
}

function htmlSupportEvents() {
    // $(".custom-file-input").on("change", function() {
    //     var fileName = $(this).val().split("\\").pop()
    //     $(this).siblings(".custom-file-label").addClass("selected").html(fileName)
    //   })

    $('#txt-search').keypress(function (e) {
        if (e.key === "Enter") {
            e.preventDefault()
            // enter has been pressed, execute a click on .js-new:
            createSearchRequest()
            $(this).blur()
        }
    })
}

function clearUploadUI() {
    $("#inputMetadataFile01").val('')
    $('#inputMetadataText01').val('')
    $('#inputMetadataFile01').siblings(".custom-file-label").removeClass("selected").html('Choose file')
    $('.popupBtns').removeAttr("disabled")
    $('.upload-progress').hide()
}

function fileUpload() {
    let uploadedFile = $('#inputMetadataFile01').prop('files')[0]
    let metadata = $('#inputMetadataText01').val()

    if (!uploadedFile || !metadata) {
        alert('Pls upload file & add file description before uploading..!!')
        return false
    }
    $('.popupBtns').attr("disabled", true)
    $('.upload-progress').show()
    let formData = new FormData()
    formData.append("filedata", uploadedFile)
    formData.append("metadata", metadata)

    fetch(fileUploadUrl, {
        method: 'POST',
        body: formData
    }).then(
        response => {
            if (!response.ok) {
                throw new Error(response.statusText);
            }
            return response
        } // if the response is a JSON object
    ).then(
        success => { // Handle the success response object
            console.log(success)
            $('#uploadModal').modal('hide')
            alert('File Uploaded Succesfully.!!')
            clearUploadUI()
        }
    ).catch(
        error => {
            $('.popupBtns').removeAttr("disabled")
            $('.upload-progress').hide()
            console.log(error) // Handle the error response object
            alert('Error uploading file..!!')
        }
    )


    console.log(uploadedFile, metadata)

    // setTimeout(() => {
    //     progress.hide()
    //     $('#uploadModal').modal('hide')
    //     alert('File Uploaded Succesfully.!!')
    //     clearUploadUI()
    // }, 3000)

}

function listFullScreen() {
    if (!document.fullscreenElement) {
        document.getElementById('list-container-id').requestFullscreen()
    } else if (document.exitFullscreen) {
        document.exitFullscreen()
    }
}

function openLoginModal() {
    username = sessionStorage.getItem('logged-user')
    if (!username) {
        $('#loginModal').modal('show')
    }
    setLoggerUserName()
}

function loginUser() {
    username = $('#txtusername').val()
    const password = $('#txtpassword').val()
    if ((username == 'internaluser' && password == 'internal@user')
        || (username == 'adminuser' && password == 'admin@user')) {
        sessionStorage.setItem('logged-user', username)
        $('#loginModal').modal('hide')
        setLoggerUserName()
    } else {
        alert('Pls enter username & password to login')
    }
}

function setLoggerUserName() {
    $('#btnuser').attr('title', `Logout: ${username}`)
}

function logout() {
    sessionStorage.removeItem('logged-user')
    window.location.reload()
}


