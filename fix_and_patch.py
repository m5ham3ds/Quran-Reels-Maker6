import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Remove the extra brace I added
content = content.replace("    } // Close outer box for LivePreview\n}", "}")

# Now match BoxWithConstraints properly
target = """    BoxWithConstraints(
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(9f / 16f)
            .clip(RoundedCornerShape(24.dp))
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A14), Color(0xFF140D07))
                )
            )
            .border(2.dp, BorderColor, RoundedCornerShape(24.dp))
    ) {"""

replacement = """    Box(
        modifier = Modifier.fillMaxWidth().height(520.dp),
        contentAlignment = Alignment.Center
    ) {
    BoxWithConstraints(
        modifier = Modifier
            .fillMaxHeight()
            .aspectRatio(9f / 16f)
            .clip(RoundedCornerShape(24.dp))
            .background(
                Brush.verticalGradient(
                    colors = listOf(Color(0xFF070A14), Color(0xFF140D07))
                )
            )
            .border(2.dp, BorderColor, RoundedCornerShape(24.dp))
    ) {"""

if target in content:
    content = content.replace(target, replacement)
    
    # We successfully wrapped it, so now we must add the closing brace properly
    # Let's find the `}` that closes LivePreviewContainer.
    # We know LivePreviewContainer ends before `@Composable\nfun GeneratedMetaSection`
    
    end_target = """        }
    }
}

@Composable
fun GeneratedMetaSection"""

    end_replacement = """        }
    }
    } // Close Box(height=520.dp)
}

@Composable
fun GeneratedMetaSection"""

    if end_target in content:
        content = content.replace(end_target, end_replacement)
    else:
        # Fallback 1
        end_target_2 = """        }
    }
}
@Composable
fun GeneratedMetaSection"""
        end_replacement_2 = """        }
    }
    } // Close Box(height=520.dp)
}
@Composable
fun GeneratedMetaSection"""
        if end_target_2 in content:
            content = content.replace(end_target_2, end_replacement_2)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)

