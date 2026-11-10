SELECT ten FROM sinhvien s
WHERE EXISTS (SELECT 1 FROM dangky d
              WHERE d.msv = s.msv AND d.mamon = 'TOANROIRAC');
