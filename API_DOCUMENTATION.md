# Speed Camera API Documentation

**Base URL:** `https://speedcameraapi.onrender.com`

**Version:** 1.0.0

## 📖 Overview

The Speed Camera API provides a RESTful interface for managing speed camera data across the United States. Speed cameras are indexed by their intersection (two cross streets) and zipcode, making it easy to query and manage camera locations.

## 🔗 Interactive Documentation

- **Swagger UI:** [https://speedcameraapi.onrender.com/docs](https://speedcameraapi.onrender.com/docs)
- **ReDoc:** [https://speedcameraapi.onrender.com/redoc](https://speedcameraapi.onrender.com/redoc)
- **OpenAPI Spec:** [https://speedcameraapi.onrender.com/openapi.json](https://speedcameraapi.onrender.com/openapi.json)

---

## 📋 API Endpoints

### 1. Get Cameras by Zipcode

**Endpoint:** `GET /cameras/zipcode/{zipcode}`

Retrieve all speed cameras in a specific zipcode.

**Parameters:**
- `zipcode` (path parameter) - 5-digit US zipcode

**Example Request:**
```bash
curl https://speedcameraapi.onrender.com/cameras/zipcode/10001
```

**Example Response:**
```json
[
  {
    "id": 2,
    "cross_street_1": "Broadway",
    "cross_street_2": "W 34th St",
    "zipcode": "10001",
    "speed_limit": 25,
    "direction": "S"
  }
]
```

**Response Codes:**
- `200 OK` - Success (returns empty array `[]` if no cameras found)
- `400 Bad Request` - Invalid zipcode format

---

### 2. Search Cameras by Street and Zipcode

**Endpoint:** `GET /cameras/search`

Find cameras where a street name appears in either cross street within a specific zipcode.

**Query Parameters:**
- `street` (required) - Street name to search (partial match, case-insensitive)
- `zipcode` (required) - 5-digit US zipcode

**Example Request:**
```bash
curl "https://speedcameraapi.onrender.com/cameras/search?street=Broadway&zipcode=10001"
```

**Example Response:**
```json
[
  {
    "id": 2,
    "cross_street_1": "Broadway",
    "cross_street_2": "W 34th St",
    "zipcode": "10001",
    "speed_limit": 25,
    "direction": "S"
  }
]
```

**Response Codes:**
- `200 OK` - Success (returns empty array `[]` if no cameras found)
- `400 Bad Request` - Missing parameters or invalid zipcode

---

### 3. Create a New Camera

**Endpoint:** `POST /cameras`

Add a new speed camera to the database.

**Request Body:**
```json
{
  "cross_street_1": "7th Ave",
  "cross_street_2": "W 50th St",
  "zipcode": "10019",
  "speed_limit": 25,
  "direction": "N"
}
```

**Field Requirements:**
- `cross_street_1` - First cross street (1-100 characters, use abbreviations: St, Ave, Blvd, Dr)
- `cross_street_2` - Second cross street (1-100 characters)
- `zipcode` - 5-digit US zipcode (string)
- `speed_limit` - Speed limit in mph (integer, 5-85)
- `direction` - Camera direction (must be: N, S, E, W, NE, NW, SE, SW)

**Example Request:**
```bash
curl -X POST https://speedcameraapi.onrender.com/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "cross_street_1": "7th Ave",
    "cross_street_2": "W 50th St",
    "zipcode": "10019",
    "speed_limit": 25,
    "direction": "N"
  }'
```

**Example Response:**
```json
{
  "id": 11,
  "cross_street_1": "7th Ave",
  "cross_street_2": "W 50th St",
  "zipcode": "10019",
  "speed_limit": 25,
  "direction": "N"
}
```

**Response Codes:**
- `201 Created` - Camera successfully created
- `400 Bad Request` - Invalid data or duplicate camera at same intersection

---

### 4. Update a Camera

**Endpoint:** `PUT /cameras/{camera_id}`

Update an existing camera's information. All fields are optional - only provide fields you want to change.

**Parameters:**
- `camera_id` (path parameter) - Camera ID (obtained from GET requests)

**Request Body:**
```json
{
  "speed_limit": 30
}
```

**Example Request:**
```bash
curl -X PUT https://speedcameraapi.onrender.com/cameras/11 \
  -H "Content-Type: application/json" \
  -d '{
    "speed_limit": 30,
    "direction": "NE"
  }'
```

**Example Response:**
```json
{
  "id": 11,
  "cross_street_1": "7th Ave",
  "cross_street_2": "W 50th St",
  "zipcode": "10019",
  "speed_limit": 30,
  "direction": "NE"
}
```

**Response Codes:**
- `200 OK` - Camera successfully updated
- `400 Bad Request` - Invalid data
- `404 Not Found` - Camera ID doesn't exist

---

### 5. Delete a Camera

**Endpoint:** `DELETE /cameras/{camera_id}`

Permanently delete a camera from the database.

**Parameters:**
- `camera_id` (path parameter) - Camera ID (obtained from GET requests)

**Example Request:**
```bash
curl -X DELETE https://speedcameraapi.onrender.com/cameras/11
```

**Example Response:**
```json
{
  "message": "Camera deleted successfully"
}
```

**Response Codes:**
- `200 OK` - Camera successfully deleted
- `404 Not Found` - Camera ID doesn't exist

---

## 🧪 Testing the API

### Using Swagger UI (Easiest)

1. Visit: [https://speedcameraapi.onrender.com/docs](https://speedcameraapi.onrender.com/docs)
2. Click on any endpoint to expand it
3. Click "Try it out"
4. Fill in the parameters/request body
5. Click "Execute"
6. View the response

### Using cURL (Command Line)

**Complete workflow example:**

```bash
# 1. Get all cameras in NYC (zipcode 10001)
curl https://speedcameraapi.onrender.com/cameras/zipcode/10001

# 2. Search for cameras on Broadway in that zipcode
curl "https://speedcameraapi.onrender.com/cameras/search?street=Broadway&zipcode=10001"

# 3. Create a new camera
curl -X POST https://speedcameraapi.onrender.com/cameras \
  -H "Content-Type: application/json" \
  -d '{
    "cross_street_1": "8th Ave",
    "cross_street_2": "W 42nd St",
    "zipcode": "10036",
    "speed_limit": 25,
    "direction": "E"
  }'

# 4. Update the camera (use ID from response above)
curl -X PUT https://speedcameraapi.onrender.com/cameras/12 \
  -H "Content-Type: application/json" \
  -d '{"speed_limit": 30}'

# 5. Delete the camera
curl -X DELETE https://speedcameraapi.onrender.com/cameras/12
```

### Using JavaScript/Fetch

```javascript
// GET cameras by zipcode
const cameras = await fetch('https://speedcameraapi.onrender.com/cameras/zipcode/10001')
  .then(res => res.json());
console.log(cameras);

// POST new camera
const newCamera = await fetch('https://speedcameraapi.onrender.com/cameras', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    cross_street_1: "Park Ave",
    cross_street_2: "E 42nd St",
    zipcode: "10017",
    speed_limit: 25,
    direction: "N"
  })
}).then(res => res.json());
console.log(newCamera);

// PUT update camera
const updated = await fetch('https://speedcameraapi.onrender.com/cameras/1', {
  method: 'PUT',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ speed_limit: 30 })
}).then(res => res.json());

// DELETE camera
await fetch('https://speedcameraapi.onrender.com/cameras/1', {
  method: 'DELETE'
});
```

### Using Python Requests

```python
import requests

BASE_URL = "https://speedcameraapi.onrender.com"

# GET cameras by zipcode
response = requests.get(f"{BASE_URL}/cameras/zipcode/10001")
cameras = response.json()
print(cameras)

# Search by street
response = requests.get(
    f"{BASE_URL}/cameras/search",
    params={"street": "Broadway", "zipcode": "10001"}
)
results = response.json()

# POST new camera
new_camera = {
    "cross_street_1": "Lexington Ave",
    "cross_street_2": "E 42nd St",
    "zipcode": "10017",
    "speed_limit": 25,
    "direction": "S"
}
response = requests.post(f"{BASE_URL}/cameras", json=new_camera)
created = response.json()
print(f"Created camera with ID: {created['id']}")

# PUT update
response = requests.put(
    f"{BASE_URL}/cameras/{created['id']}",
    json={"speed_limit": 30}
)

# DELETE
response = requests.delete(f"{BASE_URL}/cameras/{created['id']}")
```

---

## 📊 Sample Data

The API comes preloaded with 10 speed cameras from major US cities:

| ID | Cross Streets | Zipcode | City | Speed Limit | Direction |
|----|---------------|---------|------|-------------|-----------|
| 1 | 5th Ave & W 42nd St | 10036 | New York, NY | 25 mph | N |
| 2 | Broadway & W 34th St | 10001 | New York, NY | 25 mph | S |
| 3 | Park Ave & E 59th St | 10022 | New York, NY | 30 mph | E |
| 4 | Madison Ave & E 72nd St | 10021 | New York, NY | 25 mph | W |
| 5 | Wilshire Blvd & S Beverly Dr | 90212 | Beverly Hills, CA | 35 mph | W |
| 6 | Sunset Blvd & N Highland Ave | 90028 | Los Angeles, CA | 35 mph | E |
| 7 | Michigan Ave & E Randolph St | 60601 | Chicago, IL | 30 mph | N |
| 8 | State St & W Madison St | 60602 | Chicago, IL | 25 mph | S |
| 9 | Market St & 5th St | 94103 | San Francisco, CA | 25 mph | NE |
| 10 | Lombard St & Hyde St | 94133 | San Francisco, CA | 15 mph | E |

---

## 📝 Data Format & Conventions

### Street Name Abbreviations
Use standard USPS abbreviations:
- **Street** → St
- **Avenue** → Ave
- **Boulevard** → Blvd
- **Drive** → Dr
- **Road** → Rd
- **Lane** → Ln
- **Court** → Ct

### Direction Abbreviations
- **North** → N
- **South** → S
- **East** → E
- **West** → W
- **Northeast** → NE
- **Northwest** → NW
- **Southeast** → SE
- **Southwest** → SW

### Zipcode Format
- Must be exactly 5 digits
- No dashes or spaces
- Example: `"10001"` (not `10001` as a number)

---

## ⚠️ Important Notes

### Duplicate Prevention
The API prevents duplicate cameras at the same intersection. A duplicate is defined as:
- Same `cross_street_1`
- Same `cross_street_2`
- Same `zipcode`

### Rate Limiting
This is a free-tier deployment on Render. The service may:
- Spin down after 15 minutes of inactivity
- Take ~30 seconds to wake up on first request
- Be slower than paid tiers

### Data Persistence
All data is stored in a PostgreSQL database and persists across deployments.

---

## 🔍 Error Handling

All errors return JSON with a `detail` field:

```json
{
  "detail": "Camera not found"
}
```

Common error scenarios:

| Error | Status Code | Cause |
|-------|-------------|-------|
| Invalid zipcode | 400 | Zipcode is not 5 digits |
| Duplicate camera | 400 | Camera already exists at intersection |
| Camera not found | 404 | Invalid camera ID |
| Missing parameters | 400 | Required query parameters not provided |
| Invalid direction | 400 | Direction not in valid list |
| Invalid speed limit | 400 | Speed limit outside 5-85 mph range |

---

## 🛠️ Technical Details

- **Framework:** FastAPI 0.109.0
- **Database:** PostgreSQL (shared with other projects)
- **Hosting:** Render (Free Tier)
- **Table Name:** `cameras`
- **Auto-generated Documentation:** Swagger UI / ReDoc

---

## 📞 Support

For issues or questions:
- Check the interactive Swagger documentation
- Review example requests in this guide
- Verify your request format matches the examples

---

## 📄 License

This API is created for educational purposes as part of a course assignment.