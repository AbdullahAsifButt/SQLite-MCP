SELECT Artist.Name, SUM(InvoiceLine.UnitPrice * InvoiceLine.Quantity) as TotalRevenue
FROM Artist
JOIN Album ON Artist.ArtistId = Album.ArtistId
JOIN Track ON Album.AlbumId = Track.AlbumId
JOIN InvoiceLine ON Track.TrackId = InvoiceLine.TrackId
GROUP BY Artist.ArtistId
ORDER BY TotalRevenue DESC
LIMIT 1