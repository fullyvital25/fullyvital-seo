PAIRS=(
'Enhance Hair (?:Density|Growth) Serum=>Hair Revival Serum'
'Enhance Hair Growth Supplements?\b=>Hair Revival Supplements'
'Enhance Hair Supplements?\b=>Hair Revival Supplements'
'Enhance Hair Vitamins=>Hair Revival Supplements'
'Enhance Hair Serum(?! 3-Pack)=>Hair Revival Serum'
'(?i)((?:alt|title)="[^"]*?)\benhance hair (?:(?:density|growth) )?serum\b(?! 3-pack)=>\1Hair Revival Serum'
'(?i)((?:alt|title)="[^"]*?)\benhance hair (?:(?:density|growth) )?(?:supplements?|vitamins)\b=>\1Hair Revival Supplements'
'(?i)(<a [^>]*href="[^"]*/products/[^"]*"[^>]*>[^<]*?)\benhance hair (?:(?:density|growth) )?serum\b(?! 3-pack)=>\1Hair Revival Serum'
'(?i)(<a [^>]*href="[^"]*/products/[^"]*"[^>]*>[^<]*?)\benhance hair (?:(?:density|growth) )?(?:supplements?|vitamins)\b=>\1Hair Revival Supplements'
)
