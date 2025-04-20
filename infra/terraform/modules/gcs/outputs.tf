output "bucket_id" {
  description = "The name of the bucket"
  value       = google_storage_bucket.weather_data.name
}

output "bucket_url" {
  description = "The URL of the bucket"
  value       = google_storage_bucket.weather_data.url
}

output "self_link" {
  description = "The self_link of the bucket"
  value       = google_storage_bucket.weather_data.self_link
}
