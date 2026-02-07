---
name: WordPress Pro
description: Theme development, hooks, plugins, and security
---

# WordPress Pro Skill

## Theme Structure

```
theme/
├── style.css           # Theme header + styles
├── functions.php       # Hooks, enqueues, setup
├── index.php           # Fallback template
├── header.php          # Header partial
├── footer.php          # Footer partial
├── single.php          # Single post
├── page.php            # Single page
├── archive.php         # Post archives
└── template-parts/     # Reusable components
```

## Hooks System

```php
// Actions - do something
add_action('wp_head', function() {
    echo '<meta name="author" content="Me">';
});

// Filters - modify something
add_filter('the_title', function($title) {
    return strtoupper($title);
});

// Remove hook
remove_action('wp_head', 'wp_generator');
```

## The Loop

```php
<?php if (have_posts()): ?>
    <?php while (have_posts()): the_post(); ?>
        <h2><?php the_title(); ?></h2>
        <?php the_content(); ?>
    <?php endwhile; ?>
<?php else: ?>
    <p>No posts found.</p>
<?php endif; ?>
```

## Custom Post Types

```php
add_action('init', function() {
    register_post_type('project', [
        'public' => true,
        'label' => 'Projects',
        'supports' => ['title', 'editor', 'thumbnail'],
        'has_archive' => true,
    ]);
});
```

## Security Best Practices

```php
// Escape output
echo esc_html($user_input);
echo esc_url($url);
echo esc_attr($attribute);

// Sanitize input
$clean = sanitize_text_field($_POST['field']);
$email = sanitize_email($_POST['email']);

// Nonce verification
wp_nonce_field('my_action');
if (!wp_verify_nonce($_POST['_wpnonce'], 'my_action')) die();
```

## WP-CLI

```bash
wp plugin install woocommerce --activate
wp user create john john@example.com --role=editor
wp db export backup.sql
wp cache flush
```

## When to Apply
Use when building WordPress themes, plugins, or customizing sites.
